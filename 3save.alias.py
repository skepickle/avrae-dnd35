embed
# Figure out the saving throw name and cvar variable name.
{{saveName = " ".join(" ".join(&ARGS&).split(" -",1)[0].split())}}
{{saveName = saveName.lower()}}
{{saveNameCVar = "savebonus_"+saveName.replace(" ","_")}}
{{saveName = saveName.title()}}
{{saveBonus = get(saveNameCVar,None)}}
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
usageInfo = """!3save help
!3save list
!3save <savename> [args...]|Rolls a saving throw for your current active character.

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

# If the saving throw specified was invalid, then output error message.
if saveBonus is None:
	out.append(f'-title "Untrained or unrecognized saving throw: {saveName}"')
	out.append(f'-f "{usageInfo}"')
	error = True

if (not error) and (take > 20):
	out.append(f'-title "Cannot take-{take} when doing a saving throw."')
	out.append(f'-f "{usageInfo}"')
	error = True

# At this point, the saving throw specified is known, and its bonus is known. Calculate throw using argument values and display results.
if (not error):
	saveBonus = int(saveBonus)
	# Construct -thumb
	if thumb is None:
		thumb = get("image",None)
	if not (thumb is None):
		out.append(f'-thumb "{thumb}"')
	# Construct -title
	if title is None:
		titleverb = f'takes {take} on' if take > 0 else "makes"
		titleSaveNameArticle = "an" if (saveName.startswith("A") or saveName.startswith("E") or saveName.startswith("I") or saveName.startswith("O")) else "a"
		numberWords = ["", "one","two","three","four", "five", "six","seven","eight","nine","ten","eleven","twelve", "thirteen", "fourteen", "fifteen","sixteen","seventeen", "eighteen","nineteen","twenty","twenty one", "twenty two", "twenty three", "twenty four", "twenty five"]
		titleSaveNameArticle = numberWords[rr] if rr > 1 else titleSaveNameArticle
		titleThrow = "saving throws" if rr > 1 else "saving throw"
		title = f'{name} {titleverb} {titleSaveNameArticle} {saveName} {titleThrow}!'
	else:
		title = title.replace("[name]", name)
		title = title.replace("[cname]", saveName)
		#TODO Replace in title: {[^}]*} with dice rolls
		#TODO Replace in title: <[^}]*> with get() call results
		#TODO Replace in title: {{[^}]*}} with get() call results
	out.append(f'-title "{title}"')

	# Process -dc and -phrase
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

	# Execute throws
	count_success = 0
	count_failure = 0
	for i in range(rr):
		d20die = str(take) if take > 0 else "1d20"
		rolli = f'{d20die} + {saveBonus}{(" + "+str(b)) if (b != 0) else ""}'
		rolli = vroll(rolli)
		diceStr = str(rolli.dice)
		result = rolli.total
		if not (dc_val is None):
			# Nat1 and Nat20 are failure and success, respectively, for saving throws!
			if (rolli.full.startswith("1d20 (**20**)")):
				count_success += 1
			elif (rolli.full.startswith("1d20 (**1**)")):
				count_failure += 1
			elif (result >= dc_val):
				count_success += 1
			else:
				count_failure += 1
		if (rr <= 1):
			text = f'-desc "{dc}{diceStr} = `{result}`{phrase_str}"'
		else:
			text = f'-f "Throw {x}|{diceStr} = `{result}`|inline"'
		out.append(text)
		x+=1

	# Report DC summary in footer
	if not (dc_val is None):
		if (count_success+count_failure) == 1:
			if count_success == 1:
				footers.append("Success!\n")
			else:
				footers.append("Failure!\n")
		else:
			footers.append(f'{count_success} Successes | {count_failure} Failures\n')
	#TODO	for extraField in extraFields:
	#TODO		out.append(f'-f "field|{extraField}"')

footers.append("Avrae 3.5e; Made by siliceous#5311")
footer = "\n".join(footers)
out.append(f'-footer "{footer}"')
return "\n".join(out)
</drac2>
