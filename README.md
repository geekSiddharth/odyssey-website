#odyssey-website
Odyssey'17 Website

### Deployment Checklist

- [] install postgresql, pip install -r requirements.txt
- [] create db, user
- [] create sensitive_data.json

### Issues

New Issues (As of Feb 11)
 1. .
 2. .

Some problems with data (won't affect deployment of non-problem events though):
 1. a-capella, battle-troupe, blind-date, can-you-duet, pwned, sumo-wrestling don't have a google form in their website folders so I am just generating form for member data for them (no additional fields)
  	**Solution** - Added sumo-wrestling, pwned, blind-date, can-you-duet in their folders. Will get a-capella and battle-troupe in a while.
 
 2. art-attack, design-360, pwned, and gupchup doesn't have team size in the doc, so form can't be generated for them
  	**Solution** - First, check their forms. Else, take details of the Team leader and contact for an alternate member.

 3. design-360 and pwned details are missing from the doc
  	**Solution** - Ignore design-360, fixed pwned.
 	
 4. Comic strip making entry missing from doc
  	**Solution** - ignore it as of now.

Other Issues
 1. For events with large number of participants, to take the data of all participants or just the team leader? 
 	**Solution** - Team leader and contact for an alternate member.

2. Decrease font-size of event-name in event-modal.html

3. Fix the fonts in register.html

4. Fix the mobile view of register.html

5. Move facebok/register button down.
