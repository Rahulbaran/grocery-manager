const newProductsForm = document.querySelector('.new__products__form');
const newProductBtn = document.querySelector('.new__product__btn');
const addProductBtn = document.querySelector('.add__product__btn');




//event handler to add new Product Form
newProductBtn.addEventListener('click', () => {
    const newProductInput = `<div class="new__product"><label><span>Product Name</span><input type="text" class="product__name" required placeholder="product name"></label><label><span>Unit</span><input type="text" class="product__unit" required placeholder="product unit"></label><label><span>Price (In Rs.)</span><input type="number" class="product__price" required placeholder="product price"></label><button type="button" class="new__product__remove__btn btn">Remove</button></div>`;
    newProductsForm.insertAdjacentHTML('afterbegin', newProductInput);
});




//event handler to remove a product form
newProductsForm.addEventListener('click', function (e) {
    const parent = (e.target.parentNode.className === "new__product" && e.target.localName === "button");
    if(parent) this.removeChild(e.target.parentNode);
});





//event handler to make a http request for sending new product data
newProductsForm.addEventListener('submit', e => {

    //1. prevent default submit behaviour
    e.preventDefault();

    
     // 2. Pushing product data in products array
    const children = e.target.children;
    const products = [];
    
    for(let i = 0; i < children.length - 1; i++) {
        const grandChildren = children[i].children;
        const product = new Array();

        for(let j = 0; j < grandChildren.length - 1; j++) {
            const input = grandChildren[j].children[1];
            product.push(input.value);
            input.value = '';
        }
        products.push(product);
    }

    
    //3. Removing product input fields
    for(let prod = 0; prod < children.length - 2; prod++) {
        newProductsForm.removeChild(newProductsForm.firstChild);
    }
    
    
    //4. post request to send products data
    const url = '/getProducts';
    const init = {
        mode : 'same-origin',
        method : 'POST',
        headers : {
            'Content-Type' : 'application/json'
        },
        body : JSON.stringify({'products' : products})
    };
    
    fetch(url, init)
    .then(res => {
        if (res.status === 200) {
            res.json()
            .then(res => {
                const products = res.newProducts;
                products.forEach(prod => console.table(prod));
            })
        }
        else console.error('Did not get the result')
    })
    .catch(() => console.error('Got the result'));

});