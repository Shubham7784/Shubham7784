function showfunc()
{
    var ele = document.getElementById('password')
    if(ele.type === 'password')
    {
        ele.type = 'text';
    }
    else{
        ele.type = 'password';
    }
}
const data = document.getElementById('data')
if(length(data)==0)
{
    appendAlert("Login Successfull","success");
}
else
{
    appendAlert(data,"Failed")
}