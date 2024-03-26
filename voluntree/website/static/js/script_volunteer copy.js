const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const sign_in_btn2 = document.querySelector("#sign-in-btn2");
const sign_up_btn2 = document.querySelector("#sign-up-btn2");
sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
});
sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
});
sign_up_btn2.addEventListener("click", () => {
    container.classList.add("sign-up-mode2");
});
sign_in_btn2.addEventListener("click", () => {
    container.classList.remove("sign-up-mode2");
});

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".sign-up-form");
    const submitBtn = document.getElementById("my-submit");
    const textToChange = document.querySelector(".title");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Відміна стандартної дії форми (перезавантаження сторінки)

        const nameInput = document.querySelector('input[name="name-register"]');
        const emailInput = document.querySelector('input[name="mail-register"]');
        const passwordInput = document.querySelector('input[name="password-register"]');
        const confirmPasswordInput = document.querySelector('input[name="password-register-confirmation"]');

        // Перевірка валідності полів форми
        if (!validateSignUpForm(nameInput.value, emailInput.value, passwordInput.value, confirmPasswordInput.value)) {
            return false; // Вихід з функції, якщо дані не валідні
        }

        // Виконання вашого коду для відправки форми на сервер або іншої обробки
        alert("Форма відправлена!"); // Приклад: відображення повідомлення
        signUpForm.submit();
    });

    function validateSignUpForm(name, email, password, confirmPassword) {
        // Перевірка на валідність даних
        if (name === '' || email === '' || password === '' || confirmPassword === '') {
            alert("Будь ласка, заповніть всі поля.");
            return false; // Форма не відправляється
        }

        if (password !== confirmPassword) {
            alert("Паролі не співпадають.");
            return false; // Форма не відправляється
        }

        if (!password.match(/^[a-zA-Z0-9]{7,}$/)) {
            alert("Пароль повинен містити щонайменше 7 символів та складатися тільки з англійських літер і цифр.");
            return false; // Форма не відправляється
        }

        if (!email.match(/^[\w][\w+._=$/{}]{1,63}[\w]@[\w._=$/{}]{1,255}\.(com|org|edu|gov|net)\.?u?a?$/)) {
            alert("Введено некоректну адресу електронної пошти.");
            return false; // Форма не відправляється
        }

        if (name.length < 3) {
            alert("Ім'я повинно містити принаймні 3 символи.");
            return false; // Форма не відправляється
        }

        // Всі дані є валідними
        return true;
    }
});
