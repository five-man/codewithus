let registerbtn = document.querySelector('.register-btn');

registerbtn.addEventListener('click', e => {
    let comment = document.querySelector('.comment-wirte').value;
    let param = {
        'comment-write': comment
      }
      $.ajax({
        url : '{% url "test" %}',
        type: 'POST',
        headers:{
            'X-CSRFTOKEN' : '{{csrf-token}}'
        },
        data: JSON.stringify(param),
        success:function(data){
            console.log(data);
        }
       });

});