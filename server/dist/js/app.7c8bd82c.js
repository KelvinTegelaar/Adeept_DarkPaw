(function(t) {
    function e(e) {
        for (var o, r, c = e[0], i = e[1], l = e[2], d = 0, h = []; d < c.length; d++) r = c[d], Object.prototype.hasOwnProperty.call(s, r) && s[r] && h.push(s[r][0]), s[r] = 0;
        for (o in i) Object.prototype.hasOwnProperty.call(i, o) && (t[o] = i[o]);
        u && u(e);
        while (h.length) h.shift()();
        return a.push.apply(a, l || []), n()
    }

    function n() {
        for (var t, e = 0; e < a.length; e++) {
            for (var n = a[e], o = !0, c = 1; c < n.length; c++) {
                var i = n[c];
                0 !== s[i] && (o = !1)
            }
            o && (a.splice(e--, 1), t = r(r.s = n[0]))
        }
        return t
    }
    var o = {},
        s = {
            app: 0
        },
        a = [];

    function r(e) {
        if (o[e]) return o[e].exports;
        var n = o[e] = {
            i: e,
            l: !1,
            exports: {}
        };
        return t[e].call(n.exports, n, n.exports, r), n.l = !0, n.exports
    }
    r.m = t, r.c = o, r.d = function(t, e, n) {
        r.o(t, e) || Object.defineProperty(t, e, {
            enumerable: !0,
            get: n
        })
    }, r.r = function(t) {
        "undefined" !== typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(t, "__esModule", {
            value: !0
        })
    }, r.t = function(t, e) {
        if (1 & e && (t = r(t)), 8 & e) return t;
        if (4 & e && "object" === typeof t && t && t.__esModule) return t;
        var n = Object.create(null);
        if (r.r(n), Object.defineProperty(n, "default", {
                enumerable: !0,
                value: t
            }), 2 & e && "string" != typeof t)
            for (var o in t) r.d(n, o, function(e) {
                return t[e]
            }.bind(null, o));
        return n
    }, r.n = function(t) {
        var e = t && t.__esModule ? function() {
            return t["default"]
        } : function() {
            return t
        };
        return r.d(e, "a", e), e
    }, r.o = function(t, e) {
        return Object.prototype.hasOwnProperty.call(t, e)
    }, r.p = "/";
    var c = window["webpackJsonp"] = window["webpackJsonp"] || [],
        i = c.push.bind(c);
    c.push = e, c = c.slice();
    for (var l = 0; l < c.length; l++) e(c[l]);
    var u = i;
    a.push([0, "chunk-vendors"]), n()
})({
    0: function(t, e, n) {
        t.exports = n("56d7")
    },
    "0501": function(t, e, n) {
        "use strict";
        var o = n("8d6a"),
            s = n.n(o);
        s.a
    },
    "111d": function(t, e, n) {},
    "119f": function(t, e, n) {},
    "1b7d": function(t, e, n) {},
    "27a9": function(t, e, n) {
        "use strict";
        var o = n("c483"),
            s = n.n(o);
        s.a
    },
    3603: function(t, e, n) {},
    "447a": function(t, e, n) {
        "use strict";
        var o = n("c603"),
            s = n.n(o);
        s.a
    },
    "56d7": function(t, e, n) {
        "use strict";
        n.r(e);
        n("fb6a"), n("e260"), n("e6cf"), n("cca6"), n("a79d");
        var o = n("2b0e"),
            s = n("f309");
        n("d4b8"), n("5363");
        o["a"].use(s["a"]);
        var a = new s["a"]({
                icons: {
                    iconfont: "mdi"
                }
            }),
            r = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("v-app", [n("HandleWebsocket"), n("HandleKeyEvent"), n("v-app-bar", {
                    staticClass: "appBar",
                    attrs: {
                        app: "",
                        dark: ""
                    }
                }, [n("div", {
                    staticClass: "d-flex align-center"
                }, [n("v-img", {
                    staticClass: "shrink mr-2",
                    attrs: {
                        alt: "Logo",
                        contain: "",
                        src: "/api/img/icons/logo.png",
                        transition: "scale-transition",
                        width: "55"
                    }
                }), n("span", {
                    staticClass: "shrink hidden-sm-and-down",
                    staticStyle: {
                        "font-size": "2rem",
                        "margin-left": ".8rem"
                    },
                    attrs: {
                        alt: "Name",
                        "min-width": "100",
                        width: "100"
                    }
                }, [t._v("Adeept DarkPaw Bot Control WebIf")])], 1), n("v-spacer"), n("ModelSelecter")], 1), n("v-content", [n("Home")], 1)], 1)
            },
            c = [],
            i = (n("ac1f"), n("466d"), function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div", {
                    staticClass: "home"
                }, [n("ControllArea")], 1)
            }),
            l = [],
            u = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div", {
                    staticClass: "area-bg"
                }, [n("div", {
                    staticClass: "area-wrapper"
                }, [n("v-container", {
                    staticClass: "controll-area"
                }, [n("v-row", [n("v-col", {
                    attrs: {
                        md: "6",
                        sm: "7",
                        xs: "12",
                        order: "6"
                    }
                }, [n("v-row", {
                    staticClass: "innerRow"
                }, [n("v-col", {
                    attrs: {
                        cols: "12"
                    }
                }, [n("ControllerSheet", {
                    attrs: {
                        modName: "Cam"
                    }
                }, [n("VedioMod")], 1)], 1), n("v-col", {
                    directives: [{
                        name: "show",
                        rawName: "v-show",
                        value: "xs" !== this.$vuetify.breakpoint.name,
                        expression: "this.$vuetify.breakpoint.name === 'xs' ? false : true"
                    }],
                    attrs: {
                        cols: "12"
                    }
                }, [n("ControllerSheet", {
                    attrs: {
                        modName: "Instruction"
                    }
                }, [n("InstructionMod")], 1)], 1)], 1)], 1), n("v-col", {
                    attrs: {
                        md: "4",
                        sm: "5",
                        xs: "12",
                        order: "9"
                    }
                }, [n("v-row", {
                    staticClass: "innerRow"
                }, [n("v-col", {
                    attrs: {
                        cols: "12"
                    }
                }, [n("ControllerSheet", {
                    attrs: {
                        modName: "Move Control"
                    }
                }, [n("MoveControlMod")], 1)], 1), n("v-col", {
                    attrs: {
                        cols: "12"
                    }
                }, [n("ControllerSheet", {
                    attrs: {
                        modName: "Head Control"
                    }
                }, [n("ArmControlMod")], 1)], 1), n("v-col", {
                    attrs: {
                        cols: "12"
                    }
                }, [n("ControllerSheet", {
                    attrs: {
                        modName: "CVFL Control"
                    }
                }, [n("CVFLMod")], 1)], 1)], 1)], 1), n("v-col", {
                    attrs: {
                        md: "2",
                        sm: "12",
                        xs: "12",
                        order: 12
                    }
                }, [n("v-row", {
                    staticClass: "innerRow"
                }, [n("v-col", {
                    attrs: {
                        md: "12",
                        sm: "3",
                        xs: "12"
                    }
                }, [n("ControllerSheet", {
                    attrs: {
                        modName: "Hard Ware"
                    }
                }, [n("StatusMod")], 1)], 1), n("v-col", {
                    attrs: {
                        md: "12",
                        sm: "4",
                        xs: "12"
                    }
                }, [n("ControllerSheet", {
                    attrs: {
                        modName: "Actions"
                    }
                }, [n("ActionsMod")], 1)], 1), n("v-col", {
                    attrs: {
                        md: "12",
                        sm: "5",
                        xs: "12"
                    }
                }, [n("v-row", {
                    staticClass: "innerRow"
                }, [n("v-col", {
                    attrs: {
                        md: "12",
                        sm: "12",
                        xs: "6"
                    }
                }, [n("ControllerSheet", {
                    attrs: {
                        modName: "FC Control"
                    }
                }, [n("FindColorMod")], 1)], 1)], 1)], 1)], 1)], 1)], 1)], 1)], 1)])
            },
            d = [],
            h = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("v-sheet", {
                    staticClass: "mod-sheet"
                }, [n("p", {
                    staticClass: "mod-title"
                }, [t._v(t._s(t.modName))]), n("div", {
                    staticClass: "mod-wrapper"
                }, [t._t("default")], 2)])
            },
            f = [],
            p = {
                name: "ControllerSheet",
                props: {
                    modName: {
                        type: String,
                        default: "No Mod Name"
                    }
                }
            },
            v = p,
            C = (n("edf9"), n("2877")),
            m = n("6544"),
            b = n.n(m),
            w = n("8dd9"),
            g = Object(C["a"])(v, h, f, !1, null, "9a8a4ade", null),
            k = g.exports;
        b()(g, {
            VSheet: w["a"]
        });
        var y = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div", {
                    staticClass: "vedio-wrapper"
                }, [n("canvas", {
                    ref: "canvas",
                    staticClass: "canvas",
                    attrs: {
                        width: "640",
                        height: "480"
                    }
                }), n("div", {
                    staticClass: "draw-area"
                })])
            },
            _ = [],
            F = {
                name: "VedioMod",
                mounted: function() {
                    var t = this;
                    setInterval((function() {
                        var e = t.$refs.canvas,
                            n = e.getContext("2d"),
                            o = new Image;
                        o.crossOrigin = "Anonymous", o.src = "http://" + location.hostname + ":5000/video_feed", o.onload = function() {
                            n.drawImage(o, 0, 0, 640, 480)
                        }
                    }), 1e3 / 24)
                },
                methods: {
                    rgbToHsv: function(t) {
                        var e = 0,
                            n = 0,
                            o = 0,
                            s = t[0],
                            a = t[1],
                            r = t[2];
                        t.sort((function(t, e) {
                            return t - e
                        }));
                        var c = t[2],
                            i = t[0];
                        return o = c / 255, n = 0 === c ? 0 : 1 - i / c, c === i ? e = 0 : c === s && a >= r ? e = (a - r) / (c - i) * 60 + 0 : c === s && a < r ? e = (a - r) / (c - i) * 60 + 360 : c === a ? e = (r - s) / (c - i) * 60 + 120 : c === r && (e = (s - a) / (c - i) * 60 + 240), e = parseInt(e), n = parseInt(100 * n), o = parseInt(100 * o), [e, n, o]
                    }
                }
            },
            S = F,
            O = (n("d874"), Object(C["a"])(S, y, _, !1, null, "2f416a62", null)),
            x = O.exports,
            V = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div", {
                    staticClass: "status-wrapper"
                }, t._l(t.chips, (function(e, o) {
                    return n("v-chip", {
                        key: o,
                        ref: "chips",
                        refInFor: !0,
                        staticClass: "ma-2 chips",
                        attrs: {
                            color: t.chipColor[o],
                            "text-color": "white"
                        }
                    }, [n("b", {
                        staticClass: "chip-title"
                    }, [t._v(t._s(e[0] + " " + e[1]))]), t._v(" " + t._s(e[2] + e[3]) + " ")])
                })), 1)
            },
            j = [],
            A = n("5530"),
            M = n("2f62"),
            E = {
                name: "ArmControlMod",
                props: {
                    title: String
                },
                data: function() {
                    return {
                        chips: [
                            ["CPU", "Temp", 50, "°C", 55, 70],
                            ["CPU", "Usage", 75, "%", 70, 85],
                            ["RAM", "Usage", 90, "%", 70, 85]
                        ],
                        infoInterval: null
                    }
                },
                computed: Object(A["a"])({
                    chipColor: function() {
                        var t = [];
                        for (var e in this.chips) this.chips[e][2] < this.chips[e][4] ? t.push("green") : this.chips[e][2] < this.chips[e][5] ? t.push("orange") : t.push("red");
                        return t
                    }
                }, Object(M["d"])(["wsResponse"])),
                watch: {
                    wsResponse: function() {
                        if ("get_info" === this.wsResponse.title) {
                            var t = this.wsResponse.data;
                            console.log(t);
                            for (var e = 0; e < this.chips.length; e++) this.$set(this.chips[e], 2, t[e])
                        }
                    }
                },
                methods: Object(A["a"])({}, Object(M["b"])(["changeWsContent"])),
                mounted: function() {
                    var t = this;
                    this.infoInterval = setInterval((function() {
                        t.changeWsContent("get_info")
                    }), 1e3)
                },
                destroyed: function() {
                    clearInterval(this.infoInterval)
                }
            },
            L = E,
            W = (n("98ed"), n("cc20")),
            I = Object(C["a"])(L, V, j, !1, null, "59672aeb", null),
            B = I.exports;
        b()(I, {
            VChip: W["a"]
        });
        var $ = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("ButtonsChild", {
                    attrs: {
                        buttons: t.buttons,
                        cols: t.cols
                    }
                })
            },
            N = [],
            P = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div", {
                    staticClass: "button-child"
                }, t._l(t.buttonsDetail, (function(e, o) {
                    return n("ControlButton", {
                        key: o,
                        style: {
                            width: t.buttonWidth
                        },
                        attrs: {
                            attr: e
                        }
                    })
                })), 1)
            },
            R = [],
            H = (n("a9e3"), function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("v-btn", {
                    class: t.buttonClass,
                    style: t.buttonStyle,
                    attrs: {
                        small: ""
                    },
                    on: {
                        mousedown: t.handleMouseDown,
                        mouseup: t.handleMouseUp,
                        touchstart: t.handleMouseDown,
                        touchend: t.handleMouseUp
                    }
                }, [t.attr.isIcon ? n("v-icon", [t._v(t._s(t.attr.content))]) : n("span", {
                    staticClass: "texts"
                }, [t._v(t._s(t.attr.content))])], 1)
            }),
            T = [],
            D = {
                name: "ControlButton",
                props: {
                    attr: Object
                },
                data: function() {
                    return {
                        buttonsDetail: null,
                        buttonClass: ["buttons", "clickable"]
                    }
                },
                computed: {
                    buttonStyle: function() {
                        return {
                            opacity: "" === this.attr.content ? 0 : ""
                        }
                    }
                },
                methods: Object(A["a"])({
                    handleMouseDown: function(t, e) {
                        "clickable" === this.buttonClass[1] ? this.changeWsContent(this.attr.sendContent) : "action" === this.buttonClass[1] && this.changeWsContent(this.attr.reversSendContent), this.attr.reversSendContent && ("clickable" === this.buttonClass[1] ? this.$set(this.buttonClass, 1, "action") : this.$set(this.buttonClass, 1, "clickable"))
                    },
                    handleMouseUp: function() {
                        this.changeWsContent(this.attr.upSendContent)
                    }
                }, Object(M["b"])(["changeWsContent"]), {}, Object(M["c"])(["setKeyEvent"])),
                mounted: function() {
                    var t = this;
                    "" === this.attr && (this.attr = {
                        isIcon: !1,
                        content: ""
                    }), this.setKeyEvent([this.attr.sendKey, function() {
                        t.changeWsContent(t.attr.sendContent)
                    }, "down"]), this.setKeyEvent([this.attr.sendKey, function() {
                        t.changeWsContent(t.attr.upSendContent)
                    }, "up"])
                }
            },
            U = D,
            K = (n("b6ce"), n("8336")),
            J = n("132d"),
            G = Object(C["a"])(U, H, T, !1, null, "0f34694c", null),
            z = G.exports;
        b()(G, {
            VBtn: K["a"],
            VIcon: J["a"]
        });
        var X = {
                name: "ButtonsChild",
                components: {
                    ControlButton: z
                },
                props: {
                    buttons: Array,
                    cols: Number
                },
                data: function() {
                    return {
                        buttonsDetail: null,
                        buttonsState: []
                    }
                },
                computed: {
                    buttonWidth: function() {
                        return 3 === this.cols ? "30%" : 4 === this.cols ? "23%" : 1 === this.cols ? "100%" : "30%"
                    }
                },
                mounted: function() {
                    var t = [];
                    for (var e in this.buttons) {
                        var n = this.buttons[e],
                            o = {
                                isIcon: !1,
                                content: "",
                                sendContent: void 0,
                                sendKey: void 0,
                                upSendContent: void 0,
                                reversSendContent: void 0
                            };
                        if ("" !== n) {
                            var s = 0;
                            for (var a in o) o[a] = n[s], s++;
                            t.push(o)
                        } else t.push(o)
                    }
                    this.buttonsDetail = t
                }
            },
            q = X,
            Q = (n("b8b6"), Object(C["a"])(q, P, R, !1, null, "55117156", null)),
            Y = Q.exports,
            Z = {
                name: "ArmControlMod",
                components: {
                    ButtonsChild: Y
                },
                data: function() {
                    return {
                        buttons: [
                            [!1, "Stand Up", "standup", 73, ""],
                            [!1, "", "", 0, ""],
                            [!1, "Head Up", "headup", 79, ""],
                            [!1, "Stay Low", "staylow", 75, ""],
                            [!1, "Home", "home", 80, "stop"],
                            [!1, "Head Down", "headdown", 76, ""]
                        ],
                        cols: 3
                    }
                }
            },
            tt = Z,
            et = Object(C["a"])(tt, $, N, !1, null, "d712c338", null),
            nt = et.exports,
            ot = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("ButtonsChild", {
                    attrs: {
                        buttons: t.buttons,
                        cols: t.cols
                    }
                })
            },
            st = [],
            at = {
                name: "ActionsMod",
                components: {
                    ButtonsChild: Y
                },
                data: function() {
                    return {
                        buttons: [
                            [!1, "Rainbow", "rainbow", "", "", "rainbow"],
                            [!1, "Breath", "breath", "", "", "breath"],
                            [!1, "Police", "police", "", "", "police"],
                            [!1, "Motion Get", "motionGet", "", "", "stopCV"],
                            [!1, "Auto Matic", "automatic", "", "", "automaticOff"],
                            [!1, "Track Line", "trackLine", "", "", "trackLineOff"]
                        ],
                        cols: 1
                    }
                }
            },
            rt = at,
            ct = Object(C["a"])(rt, ot, st, !1, null, "632b956f", null),
            it = ct.exports,
            lt = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div", [n("ButtonsChild", {
                    attrs: {
                        buttons: t.buttons,
                        cols: t.cols
                    }
                })], 1)
            },
            ut = [],
            dt = {
                name: "MoveControlMod",
                components: {
                    ButtonsChild: Y
                },
                data: function() {
                    return {
                        buttons: ["", [!0, "mdi-arrow-up-thick", "forward", 87, "DS"], "", [!0, "mdi-arrow-left-thick", "left", 65, "TS"],
                            [!0, "mdi-arrow-down-thick", "backward", 83, "DS"],
                            [!0, "mdi-arrow-right-thick", "right", 68, "TS"]
                        ],
                        cols: 3,
                        speed: 100,
                        timmer: null
                    }
                },
                methods: Object(A["a"])({}, Object(M["b"])(["changeWsContent"])),
                watch: {
                    speed: function() {
                        var t = this;
                        this.timmer && clearTimeout(this.timmer), this.timmer = setTimeout((function() {
                            t.changeWsContent("wsB " + String(t.speed))
                        }), 300)
                    }
                }
            },
            ht = dt,
            ft = n("ba0d"),
            pt = Object(C["a"])(ht, lt, ut, !1, null, "3142100c", null),
            vt = pt.exports;
        b()(pt, {
            VSlider: ft["a"]
        });
        var Ct = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div", {
                    staticClass: "CVFL-wrapper"
                }, [n("div", {
                    staticClass: "sliders"
                }, t._l(t.valuesKeys, (function(e) {
                    return n("v-slider", {
                        key: e,
                        staticClass: "mx-4 mt-1",
                        attrs: {
                            "thumb-label": "",
                            label: e,
                            "hide-details": "",
                            min: t.values[e][1],
                            max: t.values[e][2]
                        },
                        on: {
                            change: function(n) {
                                return t.handleValueChange(e)
                            }
                        },
                        model: {
                            value: t.values[e][0],
                            callback: function(n) {
                                t.$set(t.values[e], 0, n)
                            },
                            expression: "values[valueKey][0]"
                        }
                    })
                })), 1), n("div", {
                    staticClass: "CVFL-bottons"
                }, [n("ControlButton", {
                    staticClass: "button",
                    attrs: {
                        attr: t.buttonAttr
                    }
                }), n("v-btn", {
                    staticClass: "colorButton",
                    style: {
                        borderColor: t.CVFLColor
                    },
                    attrs: {
                        small: ""
                    },
                    on: {
                        click: t.handleColorChange
                    }
                }, [t._v(" color ")])], 1)])
            },
            mt = [],
            bt = (n("d3b7"), n("ddb0"), {
                name: "CVFLMod",
                components: {
                    ControlButton: z
                },
                data: function() {
                    return {
                        buttonAttr: {
                            isIcon: !1,
                            content: "start",
                            sendContent: "CVFL",
                            reversSendContent: "stopCV"
                        },
                        values: {
                            L1: [380, 0, 480],
                            L2: [440, 0, 480],
                            SP: [20, 0, 200]
                        }
                    }
                },
                computed: Object(A["a"])({
                    valuesKeys: function() {
                        var t = [];
                        for (var e in this.values) t.push(e);
                        return t
                    },
                    rgbKeys: function() {
                        var t = [];
                        for (var e in this.rgb) t.push(e);
                        return t
                    }
                }, Object(M["d"])(["CVFLColor"])),
                methods: Object(A["a"])({
                    handleColorChange: function() {
                        "#000000" === this.CVFLColor ? (this.changeCVFLColor("#FFFFFF"), this.changeWsContent("CVFLColorSet 255")) : (this.changeCVFLColor("#000000"), this.changeWsContent("CVFLColorSet 0"))
                    },
                    handleValueChange: function(t) {
                        "L1" === t ? this.changeWsContent("CVFLL1 " + this.values.L1[0]) : "L2" === t ? this.changeWsContent("CVFLL2 " + this.values.L2[0]) : "SP" === t ? this.changeWsContent("CVFLSP " + this.values.SP[0]) : "EXP" === t && this.changeWsContent("CVFLEXP " + this.values.EXP[0])
                    }
                }, Object(M["b"])(["changeWsContent"]), {}, Object(M["c"])(["changeCVFLColor"]))
            }),
            wt = bt,
            gt = (n("447a"), Object(C["a"])(wt, Ct, mt, !1, null, "bdaa26f4", null)),
            kt = gt.exports;
        b()(gt, {
            VBtn: K["a"],
            VSlider: ft["a"]
        });
        var yt = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div", {
                    staticClass: "FC-bottons"
                }, [n("ControlButton", {
                    staticClass: "button",
                    attrs: {
                        attr: t.buttonAttr
                    }
                }), n("v-menu", {
                    attrs: {
                        "close-on-content-click": !1,
                        absolute: ""
                    },
                    scopedSlots: t._u([{
                        key: "activator",
                        fn: function(e) {
                            var o = e.on;
                            return [n("v-btn", t._g({
                                staticClass: "button colorButton",
                                style: {
                                    borderColor: t.FCColor
                                },
                                attrs: {
                                    small: ""
                                }
                            }, o), [t._v(" color ")])]
                        }
                    }])
                }, [n("div", {
                    staticClass: "colorSelecter"
                }, [n("ColorPickerChild", {
                    on: {
                        colorChange: t.handleColorChange
                    }
                })], 1)])], 1)
            },
            _t = [],
            Ft = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div", {
                    staticClass: "color-picker-child"
                }, [n("v-color-picker", {
                    staticClass: "ma-2",
                    staticStyle: {
                        "background-color": "#EEEEEE"
                    },
                    attrs: {
                        "hide-mode-switch": "",
                        "hide-canvas": "",
                        "show-swatches": "",
                        swatches: t.swatches
                    },
                    model: {
                        value: t.selectedColor,
                        callback: function(e) {
                            t.selectedColor = e
                        },
                        expression: "selectedColor"
                    }
                })], 1)
            },
            St = [],
            Ot = {
                name: "",
                props: {
                    witchColor: String,
                    defaultColor: {
                        type: String,
                        default: "#000000"
                    }
                },
                data: function() {
                    return {
                        swatches: [
                            ["#FFFFFF", "#FF0000", "#AA0000"],
                            ["#CCCCCC", "#FFFF00", "#AAAA00"],
                            ["#999999", "#00FF00", "#00AA00"],
                            ["#666666", "#00FFFF", "#00AAAA"],
                            ["#333333", "#0000FF", "#0000AA"],
                            ["#000000", "#FF00FF", "#AA00AA"]
                        ],
                        selectedColor: "#000000",
                        timmer: null
                    }
                },
                watch: {
                    selectedColor: {
                        handler: function(t, e) {
                            var n = this;
                            this.timmer && clearTimeout(this.timmer), this.timmer = setTimeout((function() {
                                return n.$emit("colorChange", n.selectedColor)
                            }), 12)
                        }
                    }
                },
                mounted: function() {
                    this.selectedColor = this.defaultColor
                }
            },
            xt = Ot,
            Vt = (n("75ad"), n("03a4")),
            jt = Object(C["a"])(xt, Ft, St, !1, null, "6487a89e", null),
            At = jt.exports;
        b()(jt, {
            VColorPicker: Vt["a"]
        });
        var Mt = {
                name: "FindColorMod",
                components: {
                    ColorPickerChild: At,
                    ControlButton: z
                },
                data: function() {
                    return {
                        buttonAttr: {
                            isIcon: !1,
                            content: "start",
                            sendContent: "findColor",
                            reversSendContent: "stopCV"
                        }
                    }
                },
                computed: Object(A["a"])({}, Object(M["d"])(["FCColor"])),
                methods: Object(A["a"])({
                    handleColorChange: function(t) {
                        this.changeFCColor(t)
                    }
                }, Object(M["c"])(["changeFCColor"]), {}, Object(M["b"])(["changeWsContent"])),
                watch: {
                    FCColor: function() {
                        var t = this.RGBToHSV255(this.hexToRgba(this.FCColor));
                        this.changeWsContent({
                            title: "findColorSet",
                            data: t
                        })
                    }
                }
            },
            Et = Mt,
            Lt = (n("27a9"), n("e449")),
            Wt = Object(C["a"])(Et, yt, _t, !1, null, "bc28902a", null),
            It = Wt.exports;
        b()(Wt, {
            VBtn: K["a"],
            VMenu: Lt["a"]
        });
        var Bt = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("v-expansion-panels", {
                    staticClass: "expansion",
                    attrs: {
                        accordion: "",
                        mandatory: ""
                    },
                    model: {
                        value: t.witchOpen,
                        callback: function(e) {
                            t.witchOpen = e
                        },
                        expression: "witchOpen"
                    }
                }, [n("v-expansion-panel", [n("v-expansion-panel-header", {
                    scopedSlots: t._u([{
                        key: "default",
                        fn: function(e) {
                            var o = e.open;
                            return [n("v-row", {
                                attrs: {
                                    "no-gutters": ""
                                }
                            }, [n("v-col", {
                                attrs: {
                                    cols: "4"
                                }
                            }, [t._v("Base Control")]), t._l(t.instructContent["Base Control"][0], (function(e) {
                                return n("v-col", {
                                    key: e,
                                    staticClass: "text--secondary",
                                    attrs: {
                                        cols: "4"
                                    }
                                }, [n("v-fade-transition", {
                                    attrs: {
                                        "leave-absolute": ""
                                    }
                                }, [o ? n("span", [t._v(" " + t._s(e) + " ")]) : t._e()])], 1)
                            }))], 2)]
                        }
                    }])
                }), n("v-expansion-panel-content", [n("v-row", {
                    attrs: {
                        "no-gutters": ""
                    }
                }, [n("v-spacer"), t._l(t.instructContent["Base Control"][1], (function(e, o) {
                    return n("v-col", {
                        key: o,
                        attrs: {
                            cols: "4"
                        }
                    }, t._l(e, (function(e, o) {
                        return n("div", {
                            key: o
                        }, [t._v(" " + t._s(o) + " - " + t._s(e)), n("br")])
                    })), 0)
                }))], 2)], 1)], 1), n("v-expansion-panel", [n("v-expansion-panel-header", [t._v("About Us")]), n("v-expansion-panel-content", {
                    staticStyle: {
                        "text-indent": "2rem"
                    }
                }, [t._v(" " + t._s(t.instructContent["About Us"]) + " ")])], 1)], 1)
            },
            $t = [],
            Nt = {
                name: "InstructionMod",
                data: function() {
                    return {
                        cols: 1,
                        witchOpen: 0,
                        instructContent: {
                            "Base Control": [
                                ["Move Control", "Head Control"],
                                [{
                                    W: "move forward",
                                    A: "turn left",
                                    S: "move backward",
                                    D: "turn right"
                                }, {
                                    I: "Stand Up",
                                    K: "Stay Low",
                                    P: "Home",
                                    O: "Head up",
                                    L: "Head down"
                                }]
                            ],
                            "About Us": "Adeept is a technical service team of open source software and hardware. Dedicated to applying the Internet and the latest industrial technology in open source area, we strive to provide best hardware support and software service for general makers and electronic enthusiasts around the world. We aim to create infinite possibilities with sharing. No matter what field you are in, we can lead you into the electronic world and bring your ideas into reality.",
                            "Contact Us": "Have a technical question for Tech Support? support@adeept.com"
                        }
                    }
                }
            },
            Pt = Nt,
            Rt = (n("7c28"), n("62ad")),
            Ht = n("cd55"),
            Tt = n("49e2"),
            Dt = n("c865"),
            Ut = n("0393"),
            Kt = n("0789"),
            Jt = n("0fd9"),
            Gt = n("2fa4"),
            zt = Object(C["a"])(Pt, Bt, $t, !1, null, "d297b16e", null),
            Xt = zt.exports;
        b()(zt, {
            VCol: Rt["a"],
            VExpansionPanel: Ht["a"],
            VExpansionPanelContent: Tt["a"],
            VExpansionPanelHeader: Dt["a"],
            VExpansionPanels: Ut["a"],
            VFadeTransition: Kt["c"],
            VRow: Jt["a"],
            VSpacer: Gt["a"]
        });
        var qt = {
                name: "ControllArea",
                components: {
                    ControllerSheet: k,
                    VedioMod: x,
                    StatusMod: B,
                    ArmControlMod: nt,
                    ActionsMod: it,
                    MoveControlMod: vt,
                    CVFLMod: kt,
                    FindColorMod: It,
                    InstructionMod: Xt
                }
            },
            Qt = qt,
            Yt = (n("0501"), n("a523")),
            Zt = Object(C["a"])(Qt, u, d, !1, null, "4d7052f0", null),
            te = Zt.exports;
        b()(Zt, {
            VCol: Rt["a"],
            VContainer: Yt["a"],
            VRow: Jt["a"]
        });
        var ee = {
                name: "Home",
                components: {
                    ControllArea: te
                }
            },
            ne = ee,
            oe = Object(C["a"])(ne, i, l, !1, null, null, null),
            se = oe.exports,
            ae = function() {},
            re = [],
            ce = {
                name: "ModelSelecter",
                data: function() {
                    return {
                        items: ["Foo", "Bar", "Fizz", "Buzz"]
                    }
                }
            },
            ie = ce,
            le = (n("b5b5"), n("8860")),
            ue = n("da13"),
            de = n("5d23"),
            he = Object(C["a"])(ie, ae, re, !1, null, "55af1b4c", null),
            fe = he.exports;
        b()(he, {
            VBtn: K["a"],
            VList: le["a"],
            VListItem: ue["a"],
            VListItemTitle: de["a"],
            VMenu: Lt["a"]
        });
        var pe = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div")
            },
            ve = [],
            Ce = {
                name: "HandleWebsocket",
                data: function() {
                    return {
                        websock: null
                    }
                },
                computed: Object(A["a"])({}, Object(M["d"])(["wsContent"])),
                created: function() {
                    this.initWebSocket()
                },
                destroyed: function() {
                    this.websock.close()
                },
                methods: Object(A["a"])({
                    initWebSocket: function() {
                        console.log("now location -- " + location.hostname);
                        var t = "ws://" + location.hostname + ":8888";
                        this.websock = new WebSocket(t), this.websock.onmessage = this.websocketonmessage, this.websock.onopen = this.websocketonopen, this.websock.onerror = this.websocketonerror, this.websock.onclose = this.websocketclose
                    },
                    websocketonopen: function() {
                        this.websock.send("admin:123456")
                    },
                    websocketonerror: function() {
                        this.initWebSocket()
                    },
                    websocketonmessage: function(t) {
                        console.log("============ responseData ============");
                        var e = null;
                        try {
                            e = JSON.parse(t.data)
                        } catch (n) {
                            e = t.data, console.log("response Data not JSON")
                        }
                        console.log(e), this.changeWsResponse(e)
                    },
                    websocketsend: function(t) {
                        if (t) {
                            console.log("============ sendingData ============");
                            try {
                                t = JSON.stringify(t)
                            } catch (e) {
                                console.log("can`t send with JSON")
                            }
                            console.log(t), this.websock.send(t), this.changeWsContent("")
                        }
                    },
                    websocketclose: function(t) {
                        console.log("断开连接", t)
                    }
                }, Object(M["b"])(["changeWsResponse"]), {}, Object(M["b"])(["changeWsContent"])),
                watch: {
                    wsContent: function() {
                        this.wsContent && this.websocketsend(this.wsContent)
                    }
                }
            },
            me = Ce,
            be = Object(C["a"])(me, pe, ve, !1, null, null, null),
            we = be.exports,
            ge = function() {
                var t = this,
                    e = t.$createElement,
                    n = t._self._c || e;
                return n("div")
            },
            ke = [],
            ye = (n("38cf"), {
                name: "HandleKeyEvent",
                computed: Object(A["a"])({}, Object(M["d"])(["keyEvents"])),
                created: function() {
                    var t = this;
                    document.onkeydown = function(e) {
                        if (!e.repeat)
                            for (var n in t.keyEvents.down)
                                if (e.keyCode === Number(n)) {
                                    var o = t.keyEvents.down[n];
                                    o()
                                }
                    }, document.onkeyup = function(e) {
                        for (var n in t.keyEvents.up)
                            if (e.keyCode === Number(n)) {
                                var o = t.keyEvents.up[n];
                                o()
                            }
                    }
                }
            }),
            _e = ye,
            Fe = Object(C["a"])(_e, ge, ke, !1, null, null, null),
            Se = Fe.exports,
            Oe = {
                name: "App",
                components: {
                    Home: se,
                    ModelSelecter: fe,
                    HandleWebsocket: we,
                    HandleKeyEvent: Se
                },
                data: function() {
                    return {}
                }
            },
            xe = null != navigator.userAgent.toLowerCase().match(/(ipod|iphone|android|coolpad|mmp|smartphone|midp|wap|xoom|symbian|j2me|blackberry|wince)/i);
        xe && console.log("mobaView");
        var Ve = Oe,
            je = (n("7faf"), n("7496")),
            Ae = n("40dc"),
            Me = n("a75b"),
            Ee = n("adda"),
            Le = Object(C["a"])(Ve, r, c, !1, null, null, null),
            We = Le.exports;
        b()(Le, {
            VApp: je["a"],
            VAppBar: Ae["a"],
            VContent: Me["a"],
            VImg: Ee["a"],
            VSpacer: Gt["a"]
        });
        var Ie = n("9483");
        Object(Ie["a"])("".concat("/", "service-worker.js"), {
            ready: function() {
                console.log("App is being served from cache by a service worker.\nFor more details, visit https://goo.gl/AFskqB")
            },
            registered: function() {
                console.log("Service worker has been registered.")
            },
            cached: function() {
                console.log("Content has been cached for offline use.")
            },
            updatefound: function() {
                console.log("New content is downloading.")
            },
            updated: function() {
                console.log("New content is available; please refresh.")
            },
            offline: function() {
                console.log("No internet connection found. App is running in offline mode.")
            },
            error: function(t) {
                console.error("Error during service worker registration:", t)
            }
        });
        var Be = n("8c4f");
        o["a"].use(Be["a"]);
        var $e = [{
                path: "/",
                name: "Home",
                component: se
            }],
            Ne = new Be["a"]({
                mode: "history",
                base: "/",
                routes: $e
            }),
            Pe = Ne;
        o["a"].use(M["a"]);
        var Re = new M["a"].Store({
            state: {
                CVFLColor: "#FFFFFF",
                FCColor: "#FFFF00",
                nowAction: "none",
                wsContent: "",
                wsResponse: "",
                keyEvents: {
                    down: {},
                    up: {}
                }
            },
            actions: {
                changeWsContent: function(t, e) {
                    t.commit("changeWsContent", e)
                },
                changeWsResponse: function(t, e) {
                    e && t.commit("changeWsResponse", e)
                }
            },
            mutations: {
                changeCVFLColor: function(t, e) {
                    t.CVFLColor = e
                },
                changeFCColor: function(t, e) {
                    console.log(e), t.FCColor = e
                },
                changeWsContent: function(t, e) {
                    t.wsContent = e
                },
                changeWsResponse: function(t, e) {
                    t.wsResponse = e
                },
                setKeyEvent: function(t, e) {
                    e && e[0] && e[1] && e[2] && (t.keyEvents[e[2]][e[0]] = e[1])
                }
            },
            modules: {}
        });
        n("8ae3");
        o["a"].config.productionTip = !1, o["a"].prototype.RGBToHSV255 = function(t) {
            var e = 0,
                n = 0,
                o = 0,
                s = t[0],
                a = t[1],
                r = t[2];
            t.sort((function(t, e) {
                return t - e
            }));
            var c = t[2],
                i = t[0];
            return o = c / 255, n = 0 === c ? 0 : 1 - i / c, c === i ? e = 0 : c === s && a >= r ? e = (a - r) / (c - i) * 60 + 0 : c === s && a < r ? e = (a - r) / (c - i) * 60 + 360 : c === a ? e = (r - s) / (c - i) * 60 + 120 : c === r && (e = (s - a) / (c - i) * 60 + 240), e = parseInt(Math.floor(e / 2)), n = parseInt(255 * n), o = parseInt(255 * o), [e, n, o]
        }, o["a"].prototype.hexToRgba = function(t, e) {
            return e ? [parseInt("0x" + t.slice(1, 3)), parseInt("0x" + t.slice(3, 5)), parseInt("0x" + t.slice(5, 7)), e] : [parseInt("0x" + t.slice(1, 3)), parseInt("0x" + t.slice(3, 5)), parseInt("0x" + t.slice(5, 7))]
        }, new o["a"]({
            router: Pe,
            store: Re,
            vuetify: a,
            render: function(t) {
                return t(We)
            }
        }).$mount("#app")
    },
    "75ad": function(t, e, n) {
        "use strict";
        var o = n("119f"),
            s = n.n(o);
        s.a
    },
    "7c28": function(t, e, n) {
        "use strict";
        var o = n("c0a4"),
            s = n.n(o);
        s.a
    },
    "7faf": function(t, e, n) {
        "use strict";
        var o = n("111d"),
            s = n.n(o);
        s.a
    },
    "8ae3": function(t, e, n) {},
    "8d6a": function(t, e, n) {},
    "98ed": function(t, e, n) {
        "use strict";
        var o = n("1b7d"),
            s = n.n(o);
        s.a
    },
    af00: function(t, e, n) {},
    b5b5: function(t, e, n) {
        "use strict";
        var o = n("3603"),
            s = n.n(o);
        s.a
    },
    b6ce: function(t, e, n) {
        "use strict";
        var o = n("af00"),
            s = n.n(o);
        s.a
    },
    b8b6: function(t, e, n) {
        "use strict";
        var o = n("c24d"),
            s = n.n(o);
        s.a
    },
    c0a4: function(t, e, n) {},
    c24d: function(t, e, n) {},
    c483: function(t, e, n) {},
    c603: function(t, e, n) {},
    d874: function(t, e, n) {
        "use strict";
        var o = n("ef18"),
            s = n.n(o);
        s.a
    },
    edf9: function(t, e, n) {
        "use strict";
        var o = n("f2f1"),
            s = n.n(o);
        s.a
    },
    ef18: function(t, e, n) {},
    f2f1: function(t, e, n) {}
});
//# sourceMappingURL=app.7c8bd82c.js.map
