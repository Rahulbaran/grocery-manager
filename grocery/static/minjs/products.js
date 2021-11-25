"use strict";const newProductsForm=document.querySelector(".new__products__form"),newProductsContainer=document.querySelector(".new__products__fields__container"),newProductBtn=document.querySelector(".new__product__btn"),addProductBtn=document.querySelector(".add__product__btn"),productsTable=document.querySelector(".products__table"),productsMainContainer=document.querySelector(".products--main--container");newProductBtn.addEventListener("click",(()=>{newProductsContainer.insertAdjacentHTML("afterbegin",'<div class="new__product"><label><span>Product Name</span><input type="text" class="product__name" required placeholder="product name" title="product name should be maximum 200 characters long"></label><label><span>Unit</span><input type="text" class="product__unit" required placeholder="product unit" title="product unit should be maximum 20 characters long"></label><label><span>Price (In Rs.)</span><input type="number" class="product__price" required placeholder="product price" title="product price should be maximum 10 characters long"></label><button type="button" class="new__product__remove__btn btn">Remove</button></div>')})),newProductsContainer.addEventListener("click",(function(t){"new__product"===t.target.parentNode.className&&"button"===t.target.localName&&this.removeChild(t.target.parentNode)})),newProductsForm.addEventListener("submit",(function(t){t.preventDefault();const e=t.target.children[0].children,n=[];for(let t=0;t<e.length;t++){const r=e[t].children,o=new Array;for(let t=0;t<r.length-1;t++){const e=r[t].children[1];o.push(e.value),e.value=""}n.push(o)}const r=e.length-1;for(let t=0;t<r;t++)newProductsContainer.removeChild(newProductsContainer.firstChild);const o={mode:"same-origin",method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({products:n})};fetch("/getProducts",o).then((t=>{200===t.status?t.json().then((t=>{const e=t.newProducts,n=document.querySelector("tbody");if(e.forEach((t=>{const e=n.children.length,r=`<tr id="product--${t[0]}"><td>${e+1}</td><td>${t[1]}</td><td>${t[2]}</td><td>${t[3]}</td><td><button class="product__remove__btn btn">Remove</button></td></tr>`;n.insertAdjacentHTML("beforeend",r)})),t.alreadyExistProducts){const t='<div class="msg__container info__msg__container"><span>Some products are not added in list since they already exist</span>\n                    <button class="msg__hide__btn">&Cross;</button></div>';productsMainContainer.insertAdjacentHTML("afterbegin",t)}})):console.error("Did not get the result")})).catch((()=>console.error("Something went wrong while getting making the request")))})),productsTable.addEventListener("click",(function(t){if(t.target.classList.contains("product__remove__btn")){const e=t.target.parentNode.parentNode,n=e.id.split("--")[1],r={mode:"same-origin",method:"POST",headers:{"Content-Type":"application/json"},cache:"default",body:JSON.stringify({id:+n})};fetch("/removeProduct",r).then((t=>{200!==t.status&&console.error(t)})).catch(console.error),this.children[1].removeChild(e);const o=this.children[1].children;for(let t=1;t<=o.length;t++)o[t-1].firstElementChild.textContent=t}})),productsMainContainer.addEventListener("click",(function(t){t.target.classList.contains("msg__hide__btn")&&this.removeChild(t.target.parentNode)}));
//# sourceMappingURL=products.js.map