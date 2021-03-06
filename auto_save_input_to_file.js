// ==UserScript==
// @name         Save Input To File
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  automatically saves input pages to file
// @author       Lokno
// @match        https://adventofcode.com/2020/day/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    Number.prototype.pad = function(size) {
        var s = String(this);
        while (s.length < (size || 2)) {s = "0" + s;}
        return s;
    }

    if( document.URL.endsWith('/input') )
    {
        var url_sans_input = document.URL.slice(0,document.URL.lastIndexOf('/'))
        var day_num = parseInt(url_sans_input.slice(url_sans_input.lastIndexOf('/')+1))

        var bb = new Blob([document.body.innerText], { type: 'text/plain' });
        var a = document.createElement('a');
        a.download = 'day' + day_num.pad(2) + '_input.txt';
        a.href = window.URL.createObjectURL(bb);
        a.click();
    }
})();