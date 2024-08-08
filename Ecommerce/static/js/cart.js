var updatebtn = document.getElementsByClassName('update-card')
for(var i = 0; i<updatebtn.length; i++){
    updatebtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:',user)
        if (user == 'Anonymoususer'){
            console.log('User is not authenticated')
        }else{
            updateUserOrder(productId, action)
        }
    })
}
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/updateItem/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
                'X-CSRFToken' : csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('Data:', data)
            location: reload()
		});
}