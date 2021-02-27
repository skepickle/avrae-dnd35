embed
<drac2>
# Define usage information output
usageInfo = """!3check help
!3check list
!3check <checkname> [args...]|Rolls a check for your current active character.

__Valid Arguments__
-b      <bonus>
-dc     <dc>
-rr     <iterations>
-take   <10|20>

-phrase <flavor text>
-title  <title> _note: [name] and [cname] will be replaced automatically_
-thumb  <thumbnail URL>
-f      \\"Field Title|Field Text\\" - see `!help embed` {under construction}

Arguments surrounded in angled brackets (<args>) are mandatory, while those surrounded in square brackets ([args]) are optional. In either case, don\'t include the brackets."""

out = []
out.append(f'-title "Command usage:"')
out.append(f'-f "{usageInfo}"')
out.append(f'-footer "Avrae 3.5e; Made by siliceous#5311"')
return "\n".join(out)
</drac2>