function setLoggedInEvent() {
    const loginForm = document.querySelector('#login-form');

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener('submit', async e => {
        e.preventDefault();

        const response = await fetch('/auth/login', {
            method: 'POST',
            mode: 'cors',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
            redirect: 'follow', // manual, *follow, error
            referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
            body: JSON.stringify({ 'username': e.target.username.value, 'password': e.target.password.value }) // body data type must match "Content-Type" header
        }).catch(err => console.error(err));

        if (response.status !== 204) {
            throw Error('Wrong login credentials');
        }

        e.target.reset();

        console.log(response);
    });
}


setLoggedInEvent();
