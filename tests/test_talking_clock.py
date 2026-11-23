"""Native talking-clock sequencing and playback, without making sound."""
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import wave

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/half-life_clock.pl'
PERL = shutil.which('perl')


@unittest.skipUnless(PERL, 'Perl required')
class TalkingClockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='df-clock-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.clips = self.root / 'sound clips ; literal'
        self.clips.mkdir()
        self.record = self.root / 'played.json'
        self.player = self.root / 'audio player'
        self.player.write_text('#!' + sys.executable + '\n' + '''import json, os, stat, sys, wave
from pathlib import Path
with wave.open(sys.argv[1], 'rb') as f:
    record = dict(path=sys.argv[1], audio=f.readframes(f.getnframes()).hex(),
                  rate=f.getframerate(), channels=f.getnchannels(), width=f.getsampwidth(),
                  mode=stat.S_IMODE(os.stat(sys.argv[1]).st_mode))
Path(os.environ['CLOCK_RECORD']).write_text(json.dumps(record))
sys.exit(int(os.environ.get('CLOCK_PLAYER_EXIT', '0')))
''')
        self.player.chmod(0o700)
        self.env = os.environ.copy() | {'CLOCK_RECORD': str(self.record), 'TMPDIR': str(self.root)}

    def clip(self, name, data=b'\x80\x81\x82', rate=11025):
        path = self.clips / name
        with wave.open(str(path), 'wb') as f:
            f.setparams((1, 1, rate, 0, 'NONE', 'not compressed'))
            f.writeframes(data)
        # wave's writer omits padding for an odd final chunk; make the RIFF well-formed.
        raw = path.read_bytes()
        if len(raw) % 2:
            raw += b'\0'
            raw = raw[:4] + struct.pack('<I', len(raw) - 8) + raw[8:]
            path.write_bytes(raw)
        return data

    def run_clock(self, hour=13, minute=21):
        expression = 'require shift @ARGV; exit HalfLifeClock::play_clock(@ARGV);'
        return subprocess.run([PERL, '-e', expression, str(SCRIPT), str(self.clips),
                               str(self.player), str(hour), str(minute)], env=self.env,
                              capture_output=True, text=True, timeout=10)

    def test_every_time_selects_existing_clip_names_including_midnight_and_noon(self):
        expression = ('require shift @ARGV; for my $h (0..23) { for my $m (0..59) { '
                      'print join(",", HalfLifeClock::clips_for_time($h,$m)), "\\n"; } }')
        result = subprocess.run([PERL, '-e', expression, str(SCRIPT)],
                                capture_output=True, text=True, check=True)
        rows = result.stdout.splitlines()
        self.assertEqual(len(rows), 1440)
        allowed = {'time_is.wav', 'AM.wav', 'PM.wav'} | {
            f'{n:02d}.wav' for n in range(1, 21)} | {f'{n}.wav' for n in range(1, 10)} | {
            f'{n}.wav' for n in [30, 40, 50]}
        self.assertTrue(all(set(row.split(',')) <= allowed for row in rows))
        self.assertEqual(rows[0], 'time_is.wav,12.wav,AM.wav')
        self.assertEqual(rows[12 * 60], 'time_is.wav,12.wav,PM.wav')
        self.assertEqual(rows[13 * 60 + 21], 'time_is.wav,01.wav,20.wav,1.wav,PM.wav')
        self.assertEqual(rows[-1], 'time_is.wav,11.wav,50.wav,9.wav,PM.wav')

    def test_joins_clips_once_in_order_without_shell_expansion_or_audio_gaps(self):
        names = ['time_is.wav', '01.wav', '20.wav', '1.wav', 'PM.wav']
        expected = b''.join(self.clip(name, bytes([100 + n]) * 3) for n, name in enumerate(names))
        result = self.run_clock()
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads(self.record.read_text())
        self.assertEqual(bytes.fromhex(record['audio']), expected)
        self.assertEqual((record['channels'], record['width'], record['rate']), (1, 1, 11025))
        self.assertEqual(record['mode'], 0o600)
        self.assertFalse(Path(record['path']).exists())
        self.assertEqual(result.stdout, '')

    def test_missing_or_mismatched_clip_never_starts_playback(self):
        for name in ['time_is.wav', '01.wav', '20.wav', '1.wav']:
            self.clip(name)
        result = self.run_clock()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Cannot read clock clip', result.stderr)
        self.assertFalse(self.record.exists())
        self.clip('PM.wav', rate=22050)
        result = self.run_clock()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('different audio formats', result.stderr)
        self.assertFalse(self.record.exists())

    def test_truncated_clip_is_rejected_before_playback(self):
        self.clip('time_is.wav')
        path = self.clips / 'time_is.wav'
        path.write_bytes(path.read_bytes()[:-2])
        result = self.run_clock()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Truncated WAV', result.stderr)
        self.assertFalse(self.record.exists())

    def test_player_failure_is_reported_and_temp_audio_is_removed(self):
        for name in ['time_is.wav', '01.wav', '20.wav', '1.wav', 'PM.wav']:
            self.clip(name)
        self.env['CLOCK_PLAYER_EXIT'] = '7'
        result = self.run_clock()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Audio playback failed (exit 7)', result.stderr)
        self.assertFalse(Path(json.loads(self.record.read_text())['path']).exists())
