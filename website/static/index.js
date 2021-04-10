function deleteUser(userId){
    console.log("Deleted Note");
    fetch('/auth/delete-user', {
        method: 'POST',
        body: JSON.stringify({userId: userId})
    }).then((_res) => {
        window.location.href = "/";
    });

}

function test(x){
    console.log(x);
}