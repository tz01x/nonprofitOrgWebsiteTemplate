







  // function resizeAllvideoWindows(){

  //   elements=document.getElementsByClassName('sliderViewwindow');
  //   // console.log(elements);


  //   for (let index = 0; index < elements.length; index++) {
  //       const element = elements[index];
  //       console.log(element.offsetWidth);
  //       resize_ytIfrem(element.offsetWidth,element.children[0]);
        
  //   }

  // }

// function resize_ytIfrem(w,ytfream) {
//     // const ytfream = document.getElementById("yt_video");
//     let h = w * 0.5625;
//     ytfream.setAttribute('width', `${w - 200}`);
//     ytfream.setAttribute('height', `${h}`);

//   }

function changefont (e){

  const lists=document.querySelectorAll('span');
  for (let i = 0; i < lists.length; i++) {
    if(lists[i].style['fontFamily']==='"inherit"'){
      lists[i].style['fontFamily']="inherit";
    }
    
  }


}

window.onload=changefont();
