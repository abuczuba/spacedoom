#!/usr/bin/perl
# Speak the time using separately supplied Half-Life announcement clips.
# Replaces the user's Calomel.org clock; independently implemented for macOS.
# No game audio is distributed with these dotfiles.
use strict;
use warnings;
use FindBin;
use File::Spec;
use File::Temp ();

package HalfLifeClock;

sub clips_for_time {
    my ($hour, $minute) = @_;
    die "Invalid time\n" unless $hour =~ /^\d+$/ && $hour < 24
        && $minute =~ /^\d+$/ && $minute < 60;
    my @clips = ('time_is', sprintf('%02d', $hour % 12 || 12));
    if ($minute > 20) {
        push @clips, 10 * int($minute / 10);
        push @clips, $minute % 10 if $minute % 10;
    } elsif ($minute) {
        push @clips, sprintf('%02d', $minute);
    }
    push @clips, $hour < 12 ? 'AM' : 'PM';
    return map { "$_.wav" } @clips;
}

sub read_pcm {
    my ($path) = @_;
    open my $file, '<:raw', $path or die "Cannot read clock clip $path: $!\n";
    local $/;
    my $wav = <$file>;
    close $file or die "Cannot close clock clip $path: $!\n";
    die "Not a WAV clip: $path\n" unless length($wav) >= 12
        && substr($wav, 0, 4) eq 'RIFF' && substr($wav, 8, 4) eq 'WAVE';
    my $end = unpack('V', substr($wav, 4, 4)) + 8;
    die "Truncated WAV clip: $path\n" if $end > length($wav);
    my ($format, $pcm);
    for (my $offset = 12; $offset + 8 <= $end;) {
        my ($kind, $size) = unpack('a4V', substr($wav, $offset, 8));
        $offset += 8;
        die "Truncated WAV chunk: $path\n" if $offset + $size > $end;
        my $chunk = substr($wav, $offset, $size);
        if ($kind eq 'fmt ') {
            die "Unsupported WAV format: $path\n" unless $size >= 16 && unpack('v', $chunk) == 1;
            $format = substr($chunk, 0, 16);
        } elsif ($kind eq 'data') {
            $pcm = (defined $pcm ? $pcm : '') . $chunk;
        }
        $offset += $size + ($size % 2);
    }
    die "Missing WAV format/audio: $path\n" unless defined $format && defined $pcm && length($pcm);
    return ($format, $pcm);
}

sub play_clock {
    my ($directory, $player, $hour, $minute) = @_;
    die "Audio player unavailable: $player\n" unless -x $player;
    my ($format, $pcm);
    $pcm = '';
    # Read and validate every clip before playing anything.
    for my $name (clips_for_time($hour, $minute)) {
        my ($next_format, $audio) = read_pcm(File::Spec->catfile($directory, $name));
        die "Clock clips use different audio formats\n" if defined $format && $format ne $next_format;
        $format = $next_format;
        $pcm .= $audio;
    }
    my ($output, $path) = File::Temp::tempfile('half-life-clock-XXXXXXXX',
                                             TMPDIR => 1, SUFFIX => '.wav', UNLINK => 1);
    binmode $output;
    my $padding = length($pcm) % 2 ? "\0" : '';
    print {$output} 'RIFF', pack('V', 36 + length($pcm) + length($padding)),
        'WAVEfmt ', pack('V', 16), $format, 'data', pack('V', length($pcm)), $pcm, $padding
        or die "Cannot write clock announcement: $!\n";
    close $output or die "Cannot finish clock announcement: $!\n";
    my $result = system { $player } $player, $path;
    die "Cannot start audio player: $!\n" if $result == -1;
    die "Audio player interrupted\n" if $result & 127;
    die "Audio playback failed (exit " . ($result >> 8) . ")\n" if $result;
    return 0;
}

unless (caller) {
    my (undef, $minute, $hour) = localtime;
    my $ok = eval { play_clock(File::Spec->catdir($FindBin::Bin, 'wavs'), '/usr/bin/afplay', $hour, $minute); 1 };
    unless ($ok) { print STDERR "thetime: $@"; exit 1; }
}
1;
