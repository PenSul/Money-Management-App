Introduction
Since money is a thing, financial management becomes much more important. Because of some real-life problems such as unemployment or due to personal wants, a large sum of money may be needed. Therefore, the habit of saving money is required to counter these situations. As a result, an app for financial management will be needed.
Methodology
The app contains a total of 3 main functions, including a login GUI, an excel for data storage, graphs demonstrating all deposit and withdrawal. First, for the login GUI, both repetition and conditional structure is used for user registration. For example, repetition structure is used in sign_in() function to check each line username and password, reset_password() function to check each line username and give back the corresponding password. And conditional structure is used in sign_in_command() function to check if the username and password are valid or not. Moreover, mainly lists, tuples and dictionary are used in all functions, such as excel column titles.

Demonstration
***This app make use of NumPy, matplotlib, and pandas 1.5.3, so please run pip install NumPy, matplotlib and run pip install pandas=1.5.3
The basic idea of using this app is to treat it as an app to record your daily transactions. After registering or using the already exist account to login the app (Appendix 1), there will be 4 options for you to choose in the command prompt (Appendix 2), which include add transactions, view line/dot graph, sign out and exit. Typing 1 and pressing Enter will lead you to the imputation of transaction date, value, operation(deposit/withdrawal) and category of transaction (Appendix 3). Typing 2 and pressing Enter will show you two graph (a line graph and a dot graph) which visualize the excel table. Typing 3 and pressing Enter will basically return you back to the sign in page and typing 4 will exit the program. 

Examples of testing:
Login GUI: 
Username and password (by default) – user1, pass1 | user2, pass2
Create account will require user to input their username and password in the corresponding boxes first then click the create account button.
Forget password will require user to input their username only and then click on the forget password button. If the username exists, the bottom of GUI will show the corresponding password. 
CMD:
Choose 1-4 according to your choice.
For 1: date: TBD (e.g.: 11/26/2023 in DD/MM/YYYY format)
	Value: TBD (must be number)
	Operation: TBD (either deposit or withdrawal)
	Category: TBD (e.g., Drink, transportation, Food, Salary)
	Saving Goal: Y if you want to set a save goal, otherwise N.
For Y, it will ask you to input more info like the value of the saving goal, the start date and the end date of saving goal.
For 2: N/A, it will just show the graph, you will need to close the first graph first (line graph) 	to see the second graph (dot graph).
For 3: Sign out and go back to 1.
For 4: Exit program.

Reflection
Limitation:
Not User-independent – all users share the same excel.
Low security – password of user can be viewed in users.txt freely or the password can be tried for unlimited time.
This program is just a simple version of the existing app and it’s not perfect. Therefore, the following suggestions will be considered to improve the app further:
Low security: either encrypt the password by using some module or use a new token to login every time like google authenticator.
Not User-friendly: add a function of checking goal is accomplish or not, or by using seaborn heatmap to visualize, like the irl calendar where you can write the goal you want within the box.
