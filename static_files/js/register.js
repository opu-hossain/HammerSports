
var passwordFields = ['password1', 'password2'];
passwordFields.forEach(function(field) {
    document.getElementById(field + '-eye').addEventListener('click', function() {
        var passwordInput = document.getElementById(field);
        var passwordEye = document.getElementById(field + '-eye');
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            passwordEye.classList.add('text-indigo-500');
            passwordEye.classList.remove('text-gray-500');
            setTimeout(function() {
                passwordInput.type = "password";
                passwordEye.classList.add('text-gray-500');
                passwordEye.classList.remove('text-indigo-500');
            }, 3000); // Hide after 4 seconds
        } else {
            passwordInput.type = "password";
            passwordEye.classList.add('text-gray-500');
            passwordEye.classList.remove('text-indigo-500');
        }
    });
});
