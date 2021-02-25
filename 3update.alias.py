embed
<drac2>
out = []
out.append(f'-title "Updated sheet for {name}"')
prvSkillBonuses = list(character().cvars.keys())
newSkillBonuses = []
for descToken in get("description").split("~"):
	if descToken.startswith("skillbonus_"):
		newCvarName  = descToken.split("=",1)[0]
		newCvarValue = descToken.split("=",1)[1]
		set_cvar(newCvarName,newCvarValue)
		if prvSkillBonuses.count(newCvarName) > 0:
			prvSkillBonuses.remove(newCvarName)
out.append(f'-f "Status|Done"')
for staleSkill in prvSkillBonuses:
	delete_cvar(staleSkill)
return "\n".join(out)
</drac2>
-footer "Avrae 3.5e; Made by siliceous#5311"