function P00Start(){
    window.location.href = window.location.origin+'/PS01ModelSelect';
}
function P01Select(picFileName){
    window.location.href = window.location.origin+'/PS02Upload?picFileName='+picFileName;
}
function P02Exit(){
    window.location.href = window.location.origin+'/runExit'
}