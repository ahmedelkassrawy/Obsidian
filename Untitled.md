Customer
  → POST /tickets
  → API reads tenant_id, customer_id, message
  → API creates ticket_id
  → API starts workflow with initial state
  → Workflow validates required data
  → AI classifies the intent

FAQ / Billing Question
-> retrieve the tenants policy
-> prepare evidence

Duplicate Charge
-> ask billing system for transactions
-> workflow determinstic checks for duplicate
-> we check the refund policy (at the fact that there is a duplicate)
-> propose refund
-> reques the human approval 

Customer asking for a return of item
-> ask billing system for the date of the transaction
-> read the policy of return 
-> (if its elligble) return to customer with the issue id and the policy and approval that will be handled
-> Add to DB returns as a new return with having the tenant_id, customer_id, ticket_id, return_id and the item returned

Asking for a specific item in the website or shop
-> API takes it at the question endpoint
-> endpoint validates the input question and the customer id and the tenant 
-> API tells the workflow to then query the DB , tenants values and start
-> The response from db then returned to the AI to be better explainable to the user 

Unkown or low confidence intent -> human suport or escalation