if status is-interactive
# Commands to run in interactive sessions can go here
end
set fish_greeting
if status is-interactive
	abbr -a ff fastfetch
	abbr -a l ls
    abbr -a ll ls -alh
    abbr -a lll ls -lh
	abbr -a nv nvim
	abbr -a vim nvim
	abbr -a cls clear
end
