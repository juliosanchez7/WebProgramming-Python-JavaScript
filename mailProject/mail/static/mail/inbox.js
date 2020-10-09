document.addEventListener('DOMContentLoaded', function(){

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () =>compose_email());
  
  // By default, load the inbox
  load_mailbox('inbox');
});
//Function of alerts bootstrap
function tempAlert(msg,type)
{
  //Definition of success(green background) alert
  if(type==='success'){
    var el = document.createElement('div');

    el.className="alert alert-success";
    el.id="notification";
   el.innerHTML = msg;

   document.querySelector('#message').append(el);
   //Run animation
   el.style.animationPlayState = 'running';
   //Definition of error(red background) alert
  }else if(type==='error'){
    //Create div with classname and id
    var el = document.createElement('div');
    el.className="alert alert-danger";
    el.id="notification";
   el.innerHTML = msg;
   //Inserto div in message div
   document.querySelector('#message').append(el);
   //Run animation
   el.style.animationPlayState = 'running';
  }

}
//Compose email function
function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('form').onsubmit = () => {
    //Obtain values from form
    const recipient=document.querySelector('#compose-recipients').value;
    const subj=document.querySelector('#compose-subject').value;
    const body=document.querySelector('#compose-body').value;
    //Alerts by empty values
    if(subj===''){
      alert("subject is empty");
      return false;
    }else if (body===''){
      alert("Body message is empty");
      return false;

    }else if(recipient===''){
      alert("Recipient is empty");
    }
    else{
      //Post(send) email
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipient,
          subject: subj,
          body: body
      })
    })
    //Obtain JSON response
    .then(response => response.json())
    .then(result => {
        // Print result
        if(result.error){
          //Post alert if error appear
          tempAlert(result.error,'error')
        }
        //Post notification of success
        if(result.message=="Email sent successfully."){
          tempAlert(result.message,'success')
          //Clear values
          document.querySelector('#compose-recipients').value = '';
          document.querySelector('#compose-subject').value = '';
          document.querySelector('#compose-body').value = '';
          //Redirect to mailbox send
          load_mailbox('sent')
        }
    });
    return false;
    }
};
}
//Load mailbox function
function load_mailbox(mailbox) {
  //Obtain emails by mailbox value
  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails =>{
    if (mailbox==='inbox'){
      //Redirect to load_mails inbox
      load_emails(emails);
    }else if (mailbox==='sent'){
      //Redirect to load_mails sent
      load_sents(emails);
    }else if (mailbox==='archive'){
      //Redirect to load_mails archive
      load_emails(emails);
    }
  })
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function load_emails(email){
  //Obtain lenght JSON array
  const len=Object.keys(email).length;
  //Create differents divs with unique ids for each mail
  for (var i=0; i < len; i++){
    const post = document.createElement('div');
    post.className = 'row';
    post.id = email[i].id;
    if(email[i].read===false){
      post.style.backgroundColor="white";
    }if(email[i].read===true){
      post.style.backgroundColor="gray";
    }
    //Post div mails to HTML
    post.innerHTML = `<div class= "col-sm">${email[i].sender}</div> <div class= "col-sm">${email[i].subject}</div> 
    <div class= "col-sm">${email[i].timestamp}</div>`;
    document.querySelector('#emails-view,#posts').append(post);
  }
  //Click event for each mail
  document.addEventListener('click', event => {
  const element= event.target;
  if (element.className === 'col-sm'){
    //Obtain row id (parentElement)
    var id=element.parentElement.getAttribute('id');
    //email view
    load_email(id,false);
  }else if(element.className === 'row'){
    var id = element.getAttribute( 'id' );
    //email view
    load_email(id,false);
  }//Once true helps to solve multiple times execution of the event.
  }, {once: true});
}

function load_email(email_id, sent){
  //Show only email view and hide other sections
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  //Change read value to true for chang color background
  fetch('/emails/'+email_id, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  //Obtain email fields
  fetch('/emails/'+email_id)
  .then(response => response.json())
  .then(email => {
    // Print email
    if(sent===false){
      //Insert archive or unarchive button corresponding to the archive value on email boject
    if(email.archived===false){
      document.querySelector('#buttons').innerHTML=`<button class="btn btn-sm btn-outline-primary" id="archive"><i class="fa fa-folder"></i>Archive</button>`;
      document.querySelector('#buttons').addEventListener('click', () => archive_email(email.id), {once: true});
    }else{
      document.querySelector('#buttons').innerHTML=`<button class="btn btn-sm btn-outline-primary" id="unarchive"><i class="fa fa-folder-open"></i>Unarchive</button>`;
      document.querySelector('#buttons').addEventListener('click', () => unarchive_email(email.id), {once: true});
      
    }}else{
      document.querySelector('#buttons').innerHTML=``;
    }
    //Create reply button
    document.querySelector('#replybtn').innerHTML=`<button class="btn btn-sm btn-outline-primary" id="reply"><i class="fa fa-mail-reply"></i>Reply</button>`;
    //Click event for reply button
    document.querySelector('#replybtn').addEventListener('click', function(){ 
      document.getElementById("compose-recipients").setAttribute('value',email.sender);
      //Search for RE: field to do not overwrite this 
      //If subject already has RE: it doues not put it again
      var a=email.subject;
      var sear = a.search("RE:");
      if (sear===-1){
        document.getElementById("compose-subject").setAttribute('value','RE:'+email.subject ); 
        compose_email();
      }
      else{
        document.getElementById("compose-subject").setAttribute('value',email.subject );
        compose_email();
      }
    
    });
    //Show email on HTML page
    document.querySelector('#body-view').innerHTML=`<h5> <strong> From:</strong> ${email.sender}</h5>
    <h5> <strong>To:</strong> ${email.recipients}</h5><h5><strong>Subject: </strong>${email.subject}</h5>
     <h5><strong>Timestamp:</strong> ${email.timestamp}</h5> <hr><p> <strong> Message: </strong>${email.body}</p>`;
    document.querySelector('#reply').style.display = 'block';
});
}
//Load sents funtion (load a sents emails)
function load_sents(email){
  //Obtain lenght email array
  const len=Object.keys(email).length;
  //Display sents emails
  for (var i=0; i < len; i++){
    const post = document.createElement('div');
    post.className = 'row';
    post.id = email[i].id;
    post.innerHTML = `<div class= "col-sm">${email[i].recipients}</div> <div class= "col-sm">${email[i].subject}</div> 
    <div class= "col-sm">${email[i].timestamp}</div>`;
    document.querySelector('#emails-view,#posts, .row').append(post);
  }
  //click event for each sent email
  document.addEventListener('click', event => {
    const element= event.target;
    if(element.className === 'row' || element.className === 'col-sm'){
      if (element.className === 'col-sm'){
        var id=element.parentElement.getAttribute('id');
        //Load an sent email corresponding to their id
        load_email(id,true);
      }else{
        var id = element.getAttribute( 'id' );
        load_email(id,true);
      }
    }
    });
}
//archive email function (This archive an email)
function archive_email(emailid){
  //Show a succes notification
  tempAlert("Your email was archived",'success');
  //Change archived value to true
  fetch('/emails/'+emailid, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })  
}
//unarchive an email
function unarchive_email(emailid){
  //Show a success notification
  tempAlert("Your email was unarchived",'success');
  //Change archived value to false
  fetch('/emails/'+emailid, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
}
