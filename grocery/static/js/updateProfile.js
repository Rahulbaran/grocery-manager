'use strict'

/***************************
 * Avatar uploading related functionality
 ***************************/
const dropArea = document.querySelector('.dropArea');
const avatarForm = document.querySelector('.dropArea form');
const fileField = document.getElementById('avatar--file');
const uploadErrorMsg = document.querySelector('.dropArea .upload__error__msg');



//Preventing default behaviour
['dragover','dragenter','dragleave','drop'].forEach(event => {
    dropArea.addEventListener(event, e => {
        e.preventDefault();
    });
});


//Changing the border color when a file is dragged over/dragged enter
['dragover','dragenter'].forEach(event => {
    dropArea.addEventListener(event, () => {
        avatarForm.classList.add('highlight');
    });
});


//Setting border color of form back to default when dragged leave/drop occurs
['dragleave','drop'].forEach(event => {
    dropArea.addEventListener(event, () => {
        avatarForm.classList.remove('highlight');
    });
});




//Function to update message and font color of text after uploading picture
const updateMsg = (msg,color) => {
    uploadErrorMsg.textContent = msg
    uploadErrorMsg.style.color = color;
};


//Function to upload avatar
const uploadAvatarFunc = (pics) => {
    
    const fileTypes = ['image/jpeg','image/jpg','image/png','image/gif'];
    if(pics.length === 1 && pics[0].size <= (16 * 1024 * 1024) && fileTypes.includes(pics[0].type)) {

        //1. Storing file in formData Object
        const formData = new FormData();
        formData.append('avatar',pics[0]);

        //2. Making http request using fetch api
        const httpReq = async () => {
            const init = {
                method : 'post',
                mode : 'same-origin',
                cache : 'no-cache',
                body : formData
            };
            const response = await fetch('/uploadAvatar',init);
            if(response.ok && response.status === 200) {
                return await response.json();
            }
            else {
                uploadErrorMsg.textContent = '☹ Sorry something went wrong';
            }
        };

        //3. Using the response received from server
        httpReq()
        .then(res => {
            if (avatarForm.lastElementChild.matches('img')) {
                avatarForm.removeChild(avatarForm.lastElementChild);
            }
            const img = document.createElement('img');
            img.src = `../static/user-images/${res['pic']}`;
            avatarForm.append(img);

            updateMsg('Your profile pic has been updated','hsl(220,100%,55%)');
        })
        .catch(console.error);
    }

    else if(pics[0].size > 16 * 1024 * 1024) updateMsg('file size is greater than 16 MB','hsl(5, 100%, 50%)');
    else if(!fileTypes.includes(pics[0].type)) updateMsg('file in jpg/png/gif format is only allowed','hsl(5, 100%, 50%)');
    else updateMsg('Only one file is allowed to upload','hsl(5, 100%, 50%)');
};



//Event handler for drop Event
dropArea.addEventListener('drop', e => {
    const files = e.dataTransfer.files;
    const pics = [...files];
    uploadAvatarFunc(pics);
});



//Event handler for file field
fileField.addEventListener('change', function() {
    uploadAvatarFunc([...this.files]);
});






/****************************
 * General info updation related functionality
 ****************************/
const generalForm = document.querySelector('.general--details--form');
const nameField = document.querySelector('.name__Field');
const shopField = document.querySelector('.shopname__Field');
const locationField = document.querySelector('.location__Field');
const nameMsg = document.querySelector('.name__error__msg');
const shopMsg = document.querySelector('.shopname__error__msg');
const locationMsg = document.querySelector('.location__error__msg');
const generalFormMsg = document.querySelector('.general__form__error__msg');



const generalFormUpdateMsg = (msg,color) => {
    generalFormMsg.textContent = msg;
    generalFormMsg.style.color = color;
};


//event handler for submitting the form
generalForm.addEventListener('submit', e => {
    //1. Preventing default behaviour 
    e.preventDefault();

    //2. Checking if name field is empty and has more than 100 characters
    if (nameField.value.length < 5 || nameField.value.length > 100) {
        nameMsg.textContent = 'name should contain 5 to 100 characters';
        return;
    } 

    //3. Checking if shopname field contains more than 200 characters
    if (shopField.value.length >  200) {
        shopMsg.textContent = 'shopname should contain upto 200 characters';
        return;
    }

    //4. Checking if location field contains more than 100 characters
    if (locationField.value.length > 100) {
        locationMsg.textContent = 'location should contain upto 100 characters';
        return;
    }

    //5. Making http request to update the general Information
    const httpRequest = async () => {
        const body = JSON.stringify({
            name : nameField.value,
            shop : shopField.value,
            location : locationField.value
        });

        const init = {
            mode : 'same-origin',
            method : 'post',
            body : body,
            headers : { 'Content-Type' : 'application/json'},
            cache : 'no-cache'
        };

        const req = new Request('/updateGeneralInfo',init);
        const response = await fetch(req);

        if(response.status === 200) {
            return response.json();
        } else {
            generalFormUpdateMsg('Your details has not updated','hsl(5, 100%, 50%)');
        }
    };
    httpRequest()
    .then(() => generalFormUpdateMsg('Your details has been updated','hsl(220,100%,55%)'))
    .catch(() => generalFormUpdateMsg('Sorry something went wrong','hsl(5,100%,50%)'));
});