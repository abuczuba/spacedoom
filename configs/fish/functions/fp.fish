# fp: copy absolute path(s) to macOS clipboard. Original function used Linux xclip.
function fp
    if test (count $argv) -eq 0
        echo 'usage: fp PATH...' >&2
        return 2
    end
    for p in $argv
        realpath -- $p
    end | pbcopy
end
