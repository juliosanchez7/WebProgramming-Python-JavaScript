document.addEventListener('DOMContentLoaded', function(){
    load_index();
});
function load_index(){
    document.querySelector('form').onsubmit = () => {
    const post=document.querySelector('#compose-post').value;
    console.log(post);
    if(post===''){
        alert('Nothing to post');
    }else{
        console.log(post);
        fetch('/posts',{
            method: 'POST',
            body: JSON.stringify({
                content: post
            })
        })
        //Obtain JSON response
        .then(response => response.json())
        .then(result => {
            console.log(result);
        });
    }
    return false;
}

}