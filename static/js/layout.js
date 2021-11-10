//message hiding related functionality
const msgContainers = document.querySelectorAll('.msg__container');
const msgHideBtn = document.querySelectorAll('.msg__hide__btn');


msgHideBtn.forEach((btn,index) => {
    btn?.addEventListener('click', () => {
        msgContainers[index].style.display = 'none';
    })
});