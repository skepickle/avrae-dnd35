embed
# Figure out the skill name and cvar variable name.
{{skillName = " ".join(" ".join(&ARGS&).split(" -",1)[0].split())}}
{{skillName = skillName.lower()}}
{{skillName = skillName.replace(" (","(")}}
{{skillName = skillName.replace("( ","(")}}
{{skillName = skillName.replace(" )",")")}}
{{skillName = skillName.replace(") ",")")}}
{{skillName = "strength"     if (skillName == "str") else skillName }}
{{skillName = "dexterity"    if (skillName == "dex") else skillName }}
{{skillName = "constitution" if (skillName == "con") else skillName }}
{{skillName = "intelligence" if (skillName == "int") else skillName }}
{{skillName = "wisdom"       if (skillName == "wis") else skillName }}
{{skillName = "charisma"     if (skillName == "cha") else skillName }}
{{skillNameCVar = "skillbonus_"+skillName.replace("(","~").replace(")","").replace(" ","_")}}
{{skillNameCVar = skillNameCVar.replace("craft_","craft~").replace("knowledge_","knowledge~").replace("perform_","perform~").replace("profession_","profession~")}}
{{skillNameCVar = skillNameCVar.replace("~","_sub_")}}
{{skillName = "(".join(skillName.split(" ",1))+")" if (skillName.startswith("craft ") or skillName.startswith("knowledge ") or skillName.startswith("perform ") or skillName.startswith("profession ")) else skillName}}
{{skillName = skillName.title()}}
{{skillBonus = get(skillNameCVar,None)}}
{{arg     = argparse(&ARGS&)}}
{{b       = arg.last(     "b",  0)}}
{{dc      = arg.last(    "dc", None, int)}}
#TODO	{{extraFields  = arg.get(      "f")}}
{{phrase  = arg.last("phrase")}}
{{rr      = arg.last(    "rr",  1, int)}}
{{rr      = 25 if (rr > 25) else rr}}
{{take    = arg.last(  "take",  0, int)}}
{{thumb   = arg.last( "thumb")}}
{{title   = arg.last( "title")}}
{{x=1}}
<drac2>
# Define usage information output
usageInfo = """!3check help
!3check list
!3check <skillname> [args...]|Rolls a skill check for your current active character.

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

error = False
out = []
footers = []

# If the skill specified was invalid, not trained, or not as skill that is usable untrained, then output error message.
if skillBonus is None:
	out.append(f'-title "Untrained or unrecognized skill: {skillName}"')
	out.append(f'-f "{usageInfo}"')
	error = True

if (not error) and not (take in [0,10,20]):
	out.append(f'-title "Cannot take-{take} when doing a skill check."')
	out.append(f'-f "{usageInfo}"')
	error = True

# At this point, the skill specified is known, and its bonus is known. Calculate check using argument values and display results.
if (not error):
	skillBonus = int(skillBonus)
	if thumb is None:
		thumb = get("image",None)
	if not (thumb is None):
		out.append(f'-thumb "{thumb}"')
	if title is None:
		titleverb = f'takes {take} on' if take > 0 else "makes"
		titleskillNameArticle = "an" if (skillName.startswith("A") or skillName.startswith("E") or skillName.startswith("I") or skillName.startswith("O")) else "a"
		numberWords = ["", "one","two","three","four", "five", "six","seven","eight","nine","ten","eleven","twelve", "thirteen", "fourteen", "fifteen","sixteen","seventeen", "eighteen","nineteen","twenty","twenty one", "twenty two", "twenty three", "twenty four", "twenty five"]
		titleskillNameArticle = numberWords[rr] if rr > 1 else titleskillNameArticle
		titlecheck = "checks" if rr > 1 else "check"
		title = f'{name} {titleverb} {titleskillNameArticle} {skillName} {titlecheck}!'
	else:
		title = title.replace("[name]", name)
		title = title.replace("[cname]", skillName)
		#TODO Replace {[^}]*} with dice rolls
		#TODO Replace <[^}]*> with get() call results
		#TODO Replace {{[^}]*}} with get() call results
	out.append(f'-title "{title}"')

	dc_val = None
	if (rr > 1):
		#TODO Replace in phrase: {[^}]*} with dice rolls
		#TODO Replace in phrase: <[^}]*> with get() call results
		#TODO Replace in phrase: {{[^}]*}} with get() call results
		if (not (phrase is None)) and (not (dc is None)):
			out.append(f'-desc "**DC {dc}**\n_{phrase}_"')
			phrase = None
			dc_val = dc
			dc = None
		elif not (phrase is None):
			out.append(f'-desc "_{phrase}_"')
			phrase = None
		elif not (dc is None):
			out.append(f'-desc "**DC {dc}**"')
			dc_val = dc
			dc = None

	if phrase is None:
		phrase_str = ""
	else:
		phrase_str = "\n_"+phrase+"_"

	if dc is None:
		dc = ""
	else:
		dc_val = dc
		dc = "**DC "+dc+"**\n"

	count_success = 0
	count_failure = 0
	for i in range(rr):
		d20die = str(take) if take > 0 else "1d20"
		rolli = f'{d20die} + {skillBonus}{(" + "+str(b)) if (b != 0) else ""}'
		rolli = vroll(rolli)
		# Unbold nat1 and nat20 rolls because they mean nothing for 3.5e skill checks
		diceStr = str(rolli.dice).replace("**","")
		result = rolli.total
		if not (dc_val is None):
			if (result >= dc_val):
				count_success += 1
			else:
				count_failure += 1
		if (rr <= 1):
			text = f'-desc "{dc}{diceStr} = `{result}`{phrase_str}"'
		else:
			text = f'-f "Check {x}|{diceStr} = `{result}`|inline"'
		out.append(text)
		x+=1
	if not (dc_val is None):
		if (count_success+count_failure) == 1:
			if count_success == 1:
				footers.append("Success!\n")
			else:
				footers.append("Failure!\n")
		else:
			footers.append(f'{count_success} Successes | {count_failure} Failures\n')
	#TODO	for extraField in extraFields:
	#TODO		out.append(f'-f "omid|{extraField}"')

footers.append("Avrae 3.5e; Made by siliceous#5311")
footer = "\n".join(footers)
out.append(f'-footer "{footer}"')
return "\n".join(out)
</drac2>