var fname, mob, mail, name1, ad, msg, l1, l2, l3, da, tn, bg, otp, faci, pep;
let result = '';
function Ready(){
fname = document.getElementById('f_name').value;
mail = document.getElementById('email').value;
mob = document.getElementById('mobile').value;
name1 = mail.substring(0, mail.lastIndexOf("@"));
l1 = document.getElementById('l').value;
l2 = document.getElementById('m').value;
l3 = document.getElementById('h').value;
da = document.getElementById('doa').value;
tn = document.getElementById('tname').value;
bg = document.getElementById('bgno').value;
sn = document.getElementById('sname').value;
pkup = document.getElementById('pickup').value;
dpof = document.getElementById('doff').value;
otp = bkid(6);
}
function Ready1(){
  fname = document.getElementById('f_name').value;
  mail = document.getElementById('email').value;
  mob = document.getElementById('mobile').value;
  name1 = mail.substring(0, mail.lastIndexOf("@"));
  ft = document.getElementById('mealtype').value;
  msg = document.getElementById('msg').value;
  da = document.getElementById('doa').value;
  tn = document.getElementById('tname').value;
  bg = document.getElementById('bgno').value;
  sn = document.getElementById('sname').value;
  pep = document.getElementById('peeps').value;
  otp = bkid(6);
  }

  function Ready2(){
    fname = document.getElementById('f_name').value;
    mail = document.getElementById('email').value;
    mob = document.getElementById('mobile').value;
    name1 = mail.substring(0, mail.lastIndexOf("@"));
    msg = document.getElementById('msg').value;
    da = document.getElementById('doa').value;
    tn = document.getElementById('tname').value;
    bg = document.getElementById('bgno').value;
    sn = document.getElementById('sname').value;
    faci = document.getElementById('facility').value;
    otp = bkid(6);
    }
    

function bkid(length){
  const characters ='0123456789';
  const charactersLength = characters.length;
  for ( let i = 0; i < length; i++ ) 
  {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
 }

function insertcoolie(){
  Ready();
  firebase.database().ref('Booking/Coolie/'+name1).set({
      Name: fname,
      Mobile: mob,
      Email: mail,
      Pickup: pkup,
      Drop_Off: dpof,
      LargeBags: l1,
      MediumBags: l2,
      HandBags: l3,
      Arrival: da,
      TrainName: tn,
      BogeyNoBirthNo: bg,
      SName: sn,
      OTP: otp
  });
  Thanku();
}
function insertmeal(){
  Ready1();
  firebase.database().ref('Booking/MealOnWheel/'+name1).set({
      Name: fname,
      Mobile: mob,
      Email: mail,
      FoodType: ft,
      No_Of_People: pep, 
      Arrival: da,
      TrainName: tn,
      BogeyNoBirthNo: bg,
      SName: sn,
      Message: msg,
      OTP: otp
  });
  Thanku2();   
}
function insertmedical(){
  Ready2();
  firebase.database().ref('Booking/Medical/'+name1).set({
      Name: fname,
      Mobile: mob,
      Email: mail,
      Facility: faci,
      Arrival: da,
      TrainName: tn,
      BogeyNoBirthNo: bg,
      SName: sn,
      Message: msg,
      OTP: otp
  });
  Thanku3();   
}
function Thanku(){
  setTimeout(() => { window.location.replace("Thank_You/index.html") }, 4000);
  
    
}
function Thanku2(){
  setTimeout(() => { window.location.replace("Thank_You/index_meal.html") }, 4000);
  
    
}
function Thanku3(){
  setTimeout(() => { window.location.replace("Thank_You/index_medical.html") }, 4000);
  
    
}