pyenv init - fish | source
if status is-interactive
# Commands to run in interactive sessions can go here
end
set fish_greeting
if status is-interactive
	abbr -a l ls
    abbr -a ff 'clear \&\& fastfetch'
	abbr -a ll ls -alh
    abbr -a lll ls -lh
	abbr -a nv nvim
	abbr -a vim nvim
	abbr -a cls clear
	abbr -a ccc claude
end
abbr --add ff 'clear && fastfetch'
