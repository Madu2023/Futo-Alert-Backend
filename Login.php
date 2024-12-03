<?php
// Start the session
session_start();

// Check if the user is already logged in, then redirect to home
if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) {
    header("Location: home.php");
    exit;
}

// If login is successful, set the session variable
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Example: Check if username and password match
    $username = $_POST['username'];
    $password = $_POST['password'];

    // In real applications, you should use database checks and hashing for passwords
    if ($username === 'user' && $password === 'password') {
        $_SESSION['loggedin'] = true;
        header("Location: home.php");
        exit;
    } else {
        echo "Invalid login credentials.";
    }
}
?>

<!-- Login form -->
<form method="POST">
    Username: <input type="text" name="username"><br>
    Password: <input type="password" name="password"><br>
    <input type="submit" value="Login">
</form>
