function validateForm() {
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;
    var degree = document.getElementById('degree').value;

    if (name == "" || email == "" || phone == "" || degree == "") {
        alert("Please fill out all required fields.");
        return false;
    }

    // Add more validation checks as needed
    return true;
}
