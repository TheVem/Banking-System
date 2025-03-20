from datetime import date
today = date.today()
import mysql.connector
con=mysql.connector.connect(host='localhost',user='root',password='prashant@123',database='bank',auth_plugin='mysql_native_password')
cur=con.cursor()
print("Press 1 to Create Account")
print("Press 2 to Withdraw Amount")
print("Press 3 to Deposite Amount")
print("Press 4 to Fund Transfer")
print("Press 5 to Balance Enquiry")
print("Press 6 to Pin Changed")
print("Press 7 to Account Summary")

x=int(input("Enter Your Choice: "))

if x==1:
    s=f"select*from bank;"
    cur.execute(s)
    ct=0
    for row in cur:
        ct=ct+1
    ac="SBI"
    if ct>0:
        ct=ct+101
        ac=ac+str(ct)
    else:
        ac="SBI101"
    
    p=input("Enter Pin")
    n=input("Enter Name")
    f=input("Enter FName")
    e=input("Enter Email")
    ph=input("Enter Phone")
    g=input("Enter Gender")
    c=input("Enter Coutry")
    s=input("Enter State")
    ct=input("Enter City")
    a=input("Enter Amount")
    
    s=f"insert into bank values('{ac}','{p}','{n}','{f}','{e}','{ph}','{g}','{c}','{s}','{ct}','{a}');"
    cur.execute(s)
    con.commit()

elif x == 2:
    # Withdraw Amount
    pas = input("Enter the Pin: ")
    name = input("Enter the Name: ")
    s = f"select * from bank where name='{name}' and pin='{pas}';"
    cur.execute(s)
    account = cur.fetchone()
    
    if account:
        amount = float(input("Enter amount to withdraw: "))
        balance = float(account[10])
        if amount <= balance:
            new_balance = balance - amount
            cur.execute(f"update bank set amount='{new_balance}' where name='{name}' and pin='{pas}';")
            con.commit()
            s=f"insert into mytrans (acno,amount,dt,ds)values ('{account[0]}','{amount}','{today}','withdraw')"
            cur.execute(s)
            con.commit()
            print("Withdrawal successful. New balance:", new_balance)
        else:
            print("Insufficient funds.")
    else:
        print("Invalid PIN or account name.")

elif x == 3:
    # Deposit Amount
    pas = input("Enter the Pin: ")
    name = input("Enter the Name: ")
    s = f"select * from bank where name='{name}' and pin='{pas}';"
    cur.execute(s)
    account = cur.fetchone()
    
    if account:
        amount = float(input("Enter amount to deposit: "))
        new_balance = float(account[10]) + amount
        cur.execute(f"update bank set amount='{new_balance}' where name='{name}' and pin='{pas}';")
        con.commit()
        s=f"insert into mytrans (acno,amount,dt,ds)values ('{account[0]}','{amount}','{today}','Deposite')"
        cur.execute(s)
        con.commit()
        print("Deposit successful. New balance:", new_balance)
    else:
        print("Invalid PIN or account name.")

elif x == 4:
    # Fund Transfer
    sender_pin = input("Enter your PIN: ")
    sender_name = input("Enter your Name: ")
    s = f"select * from bank where name='{sender_name}' and pin='{sender_pin}';"
    cur.execute(s)
    sender_account = cur.fetchone()
    
    if sender_account:
        receiver_account_no = input("Enter recipient's Account Number: ")
        amount = float(input("Enter amount to transfer: "))
        if amount <= float(sender_account[10]):
            # Check recipient exists
            s = f"select * from bank where acno='{receiver_account_no}';"
            cur.execute(s)
            receiver_account = cur.fetchone()
            
            if receiver_account:
                # Deduct from sender
                new_sender_balance = float(sender_account[10]) - amount
                cur.execute(f"update bank set amount='{new_sender_balance}' where name='{sender_name}' and pin='{sender_pin}';")
                s=f"insert into mytrans (acno,amount,dt,ds)values ('{sender_account[0]}','{amount}','{today}','transfer')"
                cur.execute(s)
            
                # Add to receiver
                new_receiver_balance = float(receiver_account[10]) + amount
                cur.execute(f"update bank set amount='{new_receiver_balance}' where acno='{receiver_account_no}';")
                s=f"insert into mytrans (acno,amount,dt,ds)values ('{receiver_account_no}','{amount}','{today}','receive')"
                cur.execute(s)
                
                con.commit()
                print("Transfer successful.")
            else:
                print("Recipient account not found.")
        else:
            print("Insufficient funds.")
    else:
        print("Invalid PIN or account name.")

elif x == 5:
    # Balance Enquiry
    pas = input("Enter the Pin: ")
    name = input("Enter the Name: ")
    s = f"select amount from bank where name='{name}' and pin='{pas}';"
    cur.execute(s)
    balance = cur.fetchone()
    
    if balance:
        print("Your current balance is:", balance[0])
    else:
        print("Invalid PIN or account name.")

elif x == 6:
    # Change PIN
    old_pin = input("Enter your current PIN: ")
    name = input("Enter your Name: ")
    new_pin = input("Enter new PIN: ")
    s = f"select * from bank where name='{name}' and pin='{old_pin}';"
    cur.execute(s)
    account = cur.fetchone()
    
    if account:
        cur.execute(f"update bank set pin='{new_pin}' where name='{name}' and pin='{old_pin}';")
        con.commit()
        print("PIN changed successfully.")
    else:
        print("Invalid current PIN or account name.")

elif x == 7:
  
    pas=input("Enter the pin")
    a_no = input("Enter the account no: ")
    s = f"select * from bank where acno='{a_no}' and pin='{pas}';"
    cur.execute(s)
    account = cur.fetchone()
    if account:

        s=f"select*from mytrans where acno='{account[0]}'"
        cur.execute(s)
        print("Account Summary:")
        for row in cur:
            print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t")
        
    else:
        print("Invalid PIN or account number.")

else:
    print("Invalid choice.")
   
          
    
    
    
                        