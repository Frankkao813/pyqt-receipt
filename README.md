# PyQt recipt program - a proposal to automate the receipt issuing process

### introduction

The app currently has the following function
1. registeration: the person issuing receipt should register for an account
2. login: log into the account
3. window: the place to type details of the receipt. The window contain three fields.
    * name: The name of the client
    * item, pricing: currently, the format to type will be like this
    ```
    item1,price1
    item2,price2
    ```
    * note: If there is additional information to contain in the receipt, it can be stored here
4. (extension of 3.) After typing and press `OK`, a pdf will be generated. Like the one in `pdf_generated`. The template is from online source with minor adaptations using jinja2 commands

5. database: `users.sqlite`, `receipt.sqlite`



### Currently working on
1. database design: The following two info will be stored in database
    * the user issuing receipt: `users.sqlite`
    * the info of receipt: `receipt.sqlite`
2. making the UI look nicer
3. add check conditions

