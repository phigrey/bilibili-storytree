/*
  js code of interactive video editing page from bilibili
*/

function entry() {
  return fn_3df9(0)
}

function fn_3df9(t) {
  var r,
  i,
  o = fn_bd92,
  a = 1459707606518,
  s = 6;
  var e = '',
  n = Math.floor(0.001 * (Date.now() - a));
  return n === i ? r++ : (r = 0, i = n),
  e += o(s),
  e += o(t),
  r > 0 && (e += o(r)),
  e += o(n),
  e
}


function fn_bd92(t) {
  var s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#@';
  i = fn_091d,
  o = fn_c903;
  var e,
  n = 0,
  a = '';
  while (!e) a += o(i, s, 1),
  e = t < Math.pow(16, n + 1),
  n++;
  return a
}

function fn_091d(t) {
  for (var e = [], n = 0; n < t; n++) e.push(Math.floor(256 * Math.random()));
  return e
}

function fn_c903(t, e, n) {
  var r = (2 << Math.log(e.length - 1) / Math.LN2) - 1,
  i = Math.ceil(1.6 * r * n / e.length);
  n = + n;
  var o = '';
  while (1) for (var a = t(i), s = 0; s < i; s++) {
    var l = a[s] & r;
    if (e[l] && (o += e[l], o.length === n)) return o
  }
}

//console.log(entry())

function V(t) {
  //var e = document.cookie;
  var e = "_uuid=59435B4E-8AB5-8561-BFC8-64C2D53BA2EE94570infoc; buvid3=82BDC977-5645-4350-9192-F481DB96CA8313446infoc; sid=alz2fcov; fingerprint=e5ab5ab4157d69a3953ba19ac79d4286; buvid_fp=82BDC977-5645-4350-9192-F481DB96CA8313446infoc; buvid_fp_plain=82BDC977-5645-4350-9192-F481DB96CA8313446infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(umk~|m)~)R0J'uYkum)R|m); bp_video_offset_307463812=532757222393729723; fingerprint3=ce72efd661bf4513dd0f6ee90367cf34; fingerprint_s=15b0a72a899721f80926cd0109de4a90; bp_video_offset_627610576=534669767038514246; PVID=1; bp_t_offset_627610576=534231955248779059; LIVE_BUVID=AUTO6816229738047782; bsource=search_google; bp_video_offset_499087497=535232738469333885; SESSDATA=a98ed4ab%2C1639012897%2C562ce%2A61; bili_jct=f5e4afe89e9667f9378127045e534fad; DedeUserID=627610576; DedeUserID__ckMd5=64a3eeb8a80cda57"
  return e && decodeURIComponent(e.replace(new RegExp('(?:(?:^|.*;)\\s*' + encodeURIComponent(t).replace(/[\-\.\+\*]/g, '\\$&') + '\\s*\\=\\s*([^;]*).*$)|^.*$'), '$1')) || null
}

//console.log(V('bili_jct'))
