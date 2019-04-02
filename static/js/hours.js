function timeConvert( x["totalDuration"] ) {
var num = n;
var hours = ( x["totalDuration"] / 60);
var rhours = Math.floor(hours);
var minutes = (hours - rhours) * 60;
var rminutes = Math.round(minutes);
return "Total Duration: " num + " minutes = " + rhours + " hour(s) and " + rminutes + " minute(s).";
}
