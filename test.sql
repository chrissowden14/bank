select customer.first, admins.name from customer natural join user_to_admin  join admins where user_to_admin.aid=admins.aid;

select customer.first, checking_account.amount from customer natural join accounts natural join checking_account;

select admins.name, apr, TIM from admins join loan_account natural join loans where admins.llid=loan_account.llid;




