function P00Start(){
    window.location.href = window.location.origin+'/PS01ModelSelect';
}
function P01Select(picFileName){
    debugger
    window.location.href = window.location.origin+'/PS02Upload?picFileName='+picFileName;
}
function P02Submit(){
    debugger
    val=this.location.search.split("=")[1]
    document.getElementById("P02modalNum").value=val
}
