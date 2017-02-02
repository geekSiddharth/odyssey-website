# odyssey-website
Odyssey'17 Website

### Deployment Checklist

[] install postgresql, pip install -r requirements.txt
[] create db, user
[] create sensitive_data.json

 ### Issues

Some problems with data (won't affect deployment of non-problem events though):
 1. a-cappella, battle-troupe, blind-date, can-you-duet, pwned, sumo-wrestling don't have a google form in their website folders so I am just generating form for member data for them (no additional fields)
 2. art-attack, design-360, pwned, and gupchup doesn't have team size in the doc, so form can't be generated for them
 3. design-360 and pwned details are missing from the doc
 4. Comic strip making entry missing from doc

Other Issues
 1. For events with large number of participants, to take the data of all participants or just the team leader?


