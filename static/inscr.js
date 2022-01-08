
document.querySelector('#submit').onclick=()=>{
    
    var nom= document.querySelector('#nom');
    var prenom=document.querySelector('#prenom')
    var Email= document.querySelector('#Email')
    var téléphone= document.querySelector('#téléphone')
    if(nom!='' && prenom!='' && Email!='' && téléphone!='' ){
        swal({
                title: "votre inscription a été acceptée avec succès",
                text: "Vous devez vous présenter a l'école pour confirmer votre inscription",
                icon: "success",
                button: "OK",
          });}
  
    };








 