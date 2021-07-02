function validation()
{
	var pass1 = document.signupForm.userPassword;
	var pass2 = document.signupForm.userPassword2;
	var name = document.signupForm.userName;
	var email = document.signupForm.userEmail;
	if(checkAll(name,email,pass1,pass2)){	
		if(passValidation(pass1,pass2,8,16)){
			if(nameValid(name)){
				if(validateEmail(email)){
				}
			}
		}
	}
	return false;
}

function checkAll(name,email,pass1,pass2)
{
	var pass1_len = pass1.value.length;
	var pass2_len = pass2.value.length;
	if (pass1_len == 0) {
		pass1.classList.add("border-danger");
	}
	if (pass2_len == 0){
		pass2.classList.add("border-danger");
	}
	if (name.value.length == 0) { 
		name.classList.add("border-danger");
	}
	if (email.value.length == 0) { 
		email.classList.add("border-danger");
	}
	if (email.value.length == 0|| name.value.length == 0 || pass2_len == 0 || pass1_len == 0) {
		alert("Fill out all fields");
	}
}

function passValidation(pass1,pass2,mx,my)
{
	var pass1_len = pass1.value.length;
	var pass2_len = pass2.value.length;
	if (pass1.value != pass2.value)
	{
		alert("Password do not match");
		pass2.focus();
		pass1.classList.add("border-danger");
		pass2.classList.add("border-danger");
		return false;
	}
	if (pass1_len >= my || pass1_len < mx  ||pass2_len >= my || pass2_len < mx)
	{
		pass1.classList.add("border-danger");
		pass2.classList.add("border-danger");
		alert("Password should be between "+mx+" to "+my);
		pass1.focus();
		return false;
	}
	else {
		pass1.classList.remove("border-danger");
		pass2.classList.remove("border-danger");
    }
	return true;
}

function nameValid(name)
{ 
	var letters = /^[A-Za-z]+$/;
	if(name.value.match(letters))
	{
		name.classList.remove("border-danger");
		return true;
	}
	else
	{
		name.classList.add("border-danger");
		alert('Name can not have numbers or be empty');
		name.focus();
		return false;
	}
}

function ValidateEmail(email)
{
	var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	if(email.value.match(mailformat))
	{
		email.classList.remove("border-danger");
		return true;
	}
	else
	{
		alert("You have entered an invalid email address!");
		email.classList.add("border-danger");
		email.focus();
		return false;
	}
}