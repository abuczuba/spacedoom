"""Actual first-session startup with inert replacements for user plugins."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

from deploy import Deployment

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('startup_dashboard', REPO / 'configs/tmux/agent-dashboard.py')
dashboard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard)


@unittest.skipUnless(os.environ.get('DOTFILES_INTEGRATION') == '1', 'Private tmux startup test')
class DashboardStartup(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='df-dashboard-startup-', dir='/private/tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / 'home'
        ghostty = self.home / '.config/ghostty/config.ghostty'
        ghostty.parent.mkdir(parents=True)
        ghostty.write_bytes((REPO / 'configs/ghostty/config.ghostty').read_bytes())
        self.env = os.environ.copy() | {'HOME': str(self.home), 'XDG_CONFIG_HOME': str(self.home / '.config'),
                                     'XDG_STATE_HOME': str(self.root / 'state'),
                                     'PATH': '/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin'}
        self.env.pop('TMUX', None)
        self.env.pop('TMUX_PANE', None)
        release = self.root / 'release'
        deploy = Deployment(REPO, self.home, self.root / 'unused')
        deploy.materialize(release, release, deploy.manifest())
        self.config = release / 'tmux/tmux.conf'
        source = self.config.read_text()
        theme = "set -g window-status-format '" + dashboard.TITLE_SLOT + "'\n"
        theme += "set -g window-status-current-format '" + dashboard.TITLE_SLOT + "'"
        source = source.replace("run '$HOME/.tmux/plugins/tmux-dotbar/dotbar.tmux'", theme)
        source = source.replace("run '$HOME/.tmux/plugins/tpm/tpm'", '')
        self.config.chmod(0o644)
        self.config.write_text(source)
        self.socket = str(self.root / 'server.sock')
        self.addCleanup(lambda: subprocess.run(['tmux', '-S', self.socket, 'kill-server'],
                                              env=self.env, capture_output=True))

    def tm(self, *args):
        return subprocess.check_output(['tmux', '-S', self.socket, *args], env=self.env,
                                       text=True, stderr=subprocess.PIPE, timeout=10).strip()

    def start_server(self):
        # Load into an empty -f /dev/null server BEFORE creating its first
        # session, reproducing tmux's normal initial config ordering.
        self.tm('-f', '/dev/null', 'source-file', str(self.config), ';',
                'new-session', '-d', '-s', 'startup', '/bin/sleep', '120')
        until = time.monotonic() + 5
        while time.monotonic() < until:
            if self.tm('show-options', '-gqv', '@dotfiles-attention-installed') == 'on':
                break
            time.sleep(.05)
        self.assertEqual(self.tm('show-options', '-gqv', '@dotfiles-attention-installed'), 'on')
        self.assertIn('attention --socket', self.tm('list-keys', '-T', 'prefix', 'n'))
        self.assertIn('new-window', self.tm('list-keys', '-T', 'prefix', 'c'))
        self.assertIn('next-window', self.tm('list-keys', '-T', 'prefix', 'N'))
        self.assertIn(dashboard.MONITOR, self.tm('show-hooks', '-B', '-t', 'startup'))
        hook = self.tm('show-hooks', '-g', 'session-created')
        self.assertIn('watch --socket', hook)
        self.assertIn('--pager-config', hook)

    def test_first_session_and_reconstructed_server_restore_one_monitor(self):
        self.start_server()
        first = self.tm('display-message', '-p', '#{start_time}:#{pid}')
        self.tm('kill-server')
        self.start_server()
        self.assertNotEqual(first, self.tm('display-message', '-p', '#{start_time}:#{pid}'))
        hooks = self.tm('show-hooks', '-B', '-t', 'startup')
        self.assertEqual(hooks.count(dashboard.MONITOR + '::'), 1)

    def test_later_sessions_and_bootstrap_preserve_existing_attention_binding(self):
        self.start_server()
        before = self.tm('list-keys', '-T', 'prefix')
        self.tm('new-session', '-d', '-s', 'second', '/bin/sleep', '120')
        until = time.monotonic() + 5
        while time.monotonic() < until:
            if dashboard.MONITOR in self.tm('show-hooks', '-B', '-t', 'second'):
                break
            time.sleep(.05)
        self.assertIn(dashboard.MONITOR, self.tm('show-hooks', '-B', '-t', 'second'))
        self.assertEqual(before, self.tm('list-keys', '-T', 'prefix'))
        # Repeated explicit bootstrap is idempotent and doesn't duplicate the
        # native monitor or rebind keys after initial activation.
        view = dashboard.Dashboard(self.socket, self.root / 'state',
                                   self.home / '.config/ghostty/config.ghostty')
        view.bootstrap()
        self.assertEqual(before, self.tm('list-keys', '-T', 'prefix'))
        self.assertEqual(self.tm('show-hooks', '-B', '-t', 'startup').count(dashboard.MONITOR + '::'), 1)
        self.tm('set-hook', '-g', 'session-created[882]', 'display-message user-hook')
        with self.assertRaisesRegex(ValueError, 'slot 882 is occupied'):
            view.bootstrap()
        self.assertIn('user-hook', self.tm('show-hooks', '-g', 'session-created'))
