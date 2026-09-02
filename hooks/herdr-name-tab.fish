# Name the Herdr tab from what is run in it. Agent panes are named from their
# prompts instead, by the UserPromptSubmit hook.

function __herdr_name_tab --on-event fish_preexec --description 'name the herdr tab from the command'
    test "$HERDR_ENV" = 1; or return
    type -q herdr-name-tab; or return

    herdr-name-tab $argv >/dev/null 2>&1 &
    disown
end
