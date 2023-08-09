L = 50.;

f0 = 0.2/L;

eta = 0.01/L;

xval = -0.09600000000000002;
yval = 0;
xtip = 0;
tip = 0.3/L;



//+
Point(1) = {xval, yval+eta, 0, f0};
//+
Point(2) = {xval, yval-eta, 0, f0};
//+
Point(3) = {xtip-tip, yval+eta, 0, f0};
//+
Point(4) = {xtip-tip, yval-eta, 0, f0};
//+
Point(5) = {xtip,yval,0,f0};



//+
Line(1) = {1, 3};
//+
Line(2) = {3, 5};
//+
Line(3) = {5, 4};
//+
Line(4) = {4, 2};
//+
Point(6) = {-0.09600000000000002, -0.0064, 0, f0};
//+
Point(7) = {-0.09600000000000002, -0.0128, 0, f0};
//+
Point(8) = {-0.09600000000000002, -0.019200000000000002, 0, f0};
//+
Point(9) = {-0.09600000000000002, -0.0256, 0, f0};
//+
Point(10) = {-0.09600000000000002, -0.032, 0, f0};
//+
Point(11) = {-0.09600000000000002, -0.038400000000000004, 0, f0};
//+
Point(12) = {-0.09600000000000002, -0.044800000000000006, 0, f0};
//+
Point(13) = {-0.09600000000000002, -0.0512, 0, f0};
//+
Point(14) = {-0.09600000000000002, -0.057600000000000005, 0, f0};
//+
Point(15) = {-0.09600000000000002, -0.064, 0, f0};
//+
Point(16) = {-0.09600000000000002, -0.0704, 0, f0};
//+
Point(17) = {-0.09600000000000002, -0.07680000000000001, 0, f0};
//+
Point(18) = {-0.09600000000000002, -0.0832, 0, f0};
//+
Point(19) = {-0.09600000000000002, -0.08960000000000001, 0, f0};
//+
Point(20) = {-0.08960000000000001, -0.09600000000000002, 0, f0};
//+
Point(21) = {-0.0832, -0.1024, 0, f0};
//+
Point(22) = {-0.07680000000000001, -0.10880000000000001, 0, f0};
//+
Point(23) = {-0.0704, -0.11520000000000001, 0, f0};
//+
Point(24) = {-0.064, -0.1216, 0, f0};
//+
Point(25) = {-0.057600000000000005, -0.128, 0, f0};
//+
Point(26) = {-0.0512, -0.13440000000000002, 0, f0};
//+
Point(27) = {-0.044800000000000006, -0.1408, 0, f0};
//+
Point(28) = {-0.038400000000000004, -0.1472, 0, f0};
//+
Point(29) = {-0.032, -0.15360000000000001, 0, f0};
//+
Point(30) = {-0.0256, -0.16, 0, f0};
//+
Point(31) = {-0.019200000000000002, -0.1664, 0, f0};
//+
Point(32) = {-0.0128, -0.1728, 0, f0};
//+
Point(33) = {-0.0064, -0.17920000000000003, 0, f0};
//+
Point(34) = {0.0, -0.18560000000000001, 0, f0};
//+
Point(35) = {0.0064, -0.19200000000000003, 0, f0};
//+
Point(36) = {0.0128, -0.1984, 0, f0};
//+
Point(37) = {0.019200000000000002, -0.2048, 0, f0};
//+
Point(38) = {0.0256, -0.2112, 0, f0};
//+
Point(39) = {0.032, -0.21760000000000002, 0, f0};
//+
Point(40) = {0.038400000000000004, -0.22400000000000003, 0, f0};
//+
Point(41) = {0.044800000000000006, -0.23040000000000002, 0, f0};
//+
Point(42) = {0.0512, -0.23680000000000004, 0, f0};
//+
Point(43) = {0.057600000000000005, -0.2432, 0, f0};
//+
Point(44) = {0.064, -0.24960000000000002, 0, f0};
//+
Point(45) = {0.0704, -0.256, 0, f0};
//+
Point(46) = {0.07680000000000001, -0.2624, 0, f0};
//+
Point(47) = {0.0832, -0.26880000000000004, 0, f0};
//+
Point(48) = {0.08960000000000001, -0.27520000000000006, 0, f0};
//+
Point(49) = {0.09600000000000002, -0.2816, 0, f0};
//+
Point(50) = {0.1024, -0.28800000000000003, 0, f0};
//+
Point(51) = {0.10880000000000001, -0.2944, 0, f0};
//+
Point(52) = {0.11520000000000001, -0.3008, 0, f0};
//+
Point(53) = {0.1216, -0.30720000000000003, 0, f0};
//+
Point(54) = {0.128, -0.31360000000000005, 0, f0};
//+
Point(55) = {0.13440000000000002, -0.31360000000000005, 0, f0};
//+
Point(56) = {0.1408, -0.31360000000000005, 0, f0};
//+
Point(57) = {0.1472, -0.31360000000000005, 0, f0};
//+
Point(58) = {0.15360000000000001, -0.31360000000000005, 0, f0};
//+
Point(59) = {0.16, -0.31360000000000005, 0, f0};
//+
Point(60) = {0.1664, -0.31360000000000005, 0, f0};
//+
Point(61) = {0.1728, -0.31360000000000005, 0, f0};
//+
Point(62) = {0.17920000000000003, -0.31360000000000005, 0, f0};
//+
Point(63) = {0.18560000000000001, -0.31360000000000005, 0, f0};
//+
Point(64) = {0.19200000000000003, -0.31360000000000005, 0, f0};
//+
Point(65) = {0.1984, -0.31360000000000005, 0, f0};
//+
Point(66) = {0.2048, -0.31360000000000005, 0, f0};
//+
Point(67) = {0.2112, -0.31360000000000005, 0, f0};
//+
Point(68) = {0.21760000000000002, -0.31360000000000005, 0, f0};
//+
Point(69) = {0.22400000000000003, -0.31360000000000005, 0, f0};
//+
Point(70) = {0.23040000000000002, -0.31360000000000005, 0, f0};
//+
Point(71) = {0.23680000000000004, -0.31360000000000005, 0, f0};
//+
Point(72) = {0.2432, -0.31360000000000005, 0, f0};
//+
Point(73) = {0.24960000000000002, -0.31360000000000005, 0, f0};
//+
Point(74) = {0.256, -0.31360000000000005, 0, f0};
//+
Point(75) = {0.2624, -0.31360000000000005, 0, f0};
//+
Point(76) = {0.26880000000000004, -0.31360000000000005, 0, f0};
//+
Point(77) = {0.27520000000000006, -0.31360000000000005, 0, f0};
//+
Point(78) = {0.2816, -0.31360000000000005, 0, f0};
//+
Point(79) = {0.28800000000000003, -0.31360000000000005, 0, f0};
//+
Point(80) = {0.2944, -0.31360000000000005, 0, f0};
//+
Point(81) = {0.3008, -0.31360000000000005, 0, f0};
//+
Point(82) = {0.30720000000000003, -0.31360000000000005, 0, f0};
//+
Point(83) = {0.31360000000000005, -0.31360000000000005, 0, f0};
//+
Point(84) = {0.32, -0.31360000000000005, 0, f0};
//+
Point(85) = {0.3264, -0.31360000000000005, 0, f0};
//+
Point(86) = {0.3328, -0.31360000000000005, 0, f0};
//+
Point(87) = {0.3392, -0.31360000000000005, 0, f0};
//+
Point(88) = {0.3456, -0.31360000000000005, 0, f0};
//+
Point(89) = {0.35200000000000004, -0.31360000000000005, 0, f0};
//+
Point(90) = {0.35840000000000005, -0.31360000000000005, 0, f0};
//+
Point(91) = {0.3648, -0.31360000000000005, 0, f0};
//+
Point(92) = {0.37120000000000003, -0.31360000000000005, 0, f0};
//+
Point(93) = {0.37760000000000005, -0.31360000000000005, 0, f0};
//+
Point(94) = {0.38400000000000006, -0.31360000000000005, 0, f0};
//+
Point(95) = {0.3904000000000001, -0.31360000000000005, 0, f0};
//+
Point(96) = {0.3968, -0.31360000000000005, 0, f0};
//+
Point(97) = {0.4032, -0.31360000000000005, 0, f0};
//+
Point(98) = {0.4096, -0.31360000000000005, 0, f0};
//+
Point(99) = {0.41600000000000004, -0.31360000000000005, 0, f0};
//+
Point(100) = {0.4224, -0.31360000000000005, 0, f0};
//+
Point(101) = {0.4288, -0.31360000000000005, 0, f0};
//+
Point(102) = {0.43520000000000003, -0.31360000000000005, 0, f0};
//+
Point(103) = {0.44160000000000005, -0.31360000000000005, 0, f0};
//+
Point(104) = {0.44800000000000006, -0.31360000000000005, 0, f0};
//+
Point(105) = {0.4544, -0.31360000000000005, 0, f0};
//+
Point(106) = {0.46080000000000004, -0.31360000000000005, 0, f0};
//+
Point(107) = {0.46720000000000006, -0.31360000000000005, 0, f0};
//+
Point(108) = {0.4736000000000001, -0.31360000000000005, 0, f0};
//+
Point(109) = {0.4800000000000001, -0.31360000000000005, 0, f0};
//+
Point(110) = {0.4864, -0.31360000000000005, 0, f0};
//+
Point(111) = {0.4928, -0.31360000000000005, 0, f0};
//+
Point(112) = {0.4928, 0.31360000000000005, 0, f0};
//+
Point(113) = {0.4864, 0.31360000000000005, 0, f0};
//+
Point(114) = {0.4800000000000001, 0.31360000000000005, 0, f0};
//+
Point(115) = {0.4736000000000001, 0.31360000000000005, 0, f0};
//+
Point(116) = {0.46720000000000006, 0.31360000000000005, 0, f0};
//+
Point(117) = {0.46080000000000004, 0.31360000000000005, 0, f0};
//+
Point(118) = {0.4544, 0.31360000000000005, 0, f0};
//+
Point(119) = {0.44800000000000006, 0.31360000000000005, 0, f0};
//+
Point(120) = {0.44160000000000005, 0.31360000000000005, 0, f0};
//+
Point(121) = {0.43520000000000003, 0.31360000000000005, 0, f0};
//+
Point(122) = {0.4288, 0.31360000000000005, 0, f0};
//+
Point(123) = {0.4224, 0.31360000000000005, 0, f0};
//+
Point(124) = {0.41600000000000004, 0.31360000000000005, 0, f0};
//+
Point(125) = {0.4096, 0.31360000000000005, 0, f0};
//+
Point(126) = {0.4032, 0.31360000000000005, 0, f0};
//+
Point(127) = {0.3968, 0.31360000000000005, 0, f0};
//+
Point(128) = {0.3904000000000001, 0.31360000000000005, 0, f0};
//+
Point(129) = {0.38400000000000006, 0.31360000000000005, 0, f0};
//+
Point(130) = {0.37760000000000005, 0.31360000000000005, 0, f0};
//+
Point(131) = {0.37120000000000003, 0.31360000000000005, 0, f0};
//+
Point(132) = {0.3648, 0.31360000000000005, 0, f0};
//+
Point(133) = {0.35840000000000005, 0.31360000000000005, 0, f0};
//+
Point(134) = {0.35200000000000004, 0.31360000000000005, 0, f0};
//+
Point(135) = {0.3456, 0.31360000000000005, 0, f0};
//+
Point(136) = {0.3392, 0.31360000000000005, 0, f0};
//+
Point(137) = {0.3328, 0.31360000000000005, 0, f0};
//+
Point(138) = {0.3264, 0.31360000000000005, 0, f0};
//+
Point(139) = {0.32, 0.31360000000000005, 0, f0};
//+
Point(140) = {0.31360000000000005, 0.31360000000000005, 0, f0};
//+
Point(141) = {0.30720000000000003, 0.31360000000000005, 0, f0};
//+
Point(142) = {0.3008, 0.31360000000000005, 0, f0};
//+
Point(143) = {0.2944, 0.31360000000000005, 0, f0};
//+
Point(144) = {0.28800000000000003, 0.31360000000000005, 0, f0};
//+
Point(145) = {0.2816, 0.31360000000000005, 0, f0};
//+
Point(146) = {0.27520000000000006, 0.31360000000000005, 0, f0};
//+
Point(147) = {0.26880000000000004, 0.31360000000000005, 0, f0};
//+
Point(148) = {0.2624, 0.31360000000000005, 0, f0};
//+
Point(149) = {0.256, 0.31360000000000005, 0, f0};
//+
Point(150) = {0.24960000000000002, 0.31360000000000005, 0, f0};
//+
Point(151) = {0.2432, 0.31360000000000005, 0, f0};
//+
Point(152) = {0.23680000000000004, 0.31360000000000005, 0, f0};
//+
Point(153) = {0.23040000000000002, 0.31360000000000005, 0, f0};
//+
Point(154) = {0.22400000000000003, 0.31360000000000005, 0, f0};
//+
Point(155) = {0.21760000000000002, 0.31360000000000005, 0, f0};
//+
Point(156) = {0.2112, 0.31360000000000005, 0, f0};
//+
Point(157) = {0.2048, 0.31360000000000005, 0, f0};
//+
Point(158) = {0.1984, 0.31360000000000005, 0, f0};
//+
Point(159) = {0.19200000000000003, 0.31360000000000005, 0, f0};
//+
Point(160) = {0.18560000000000001, 0.31360000000000005, 0, f0};
//+
Point(161) = {0.17920000000000003, 0.31360000000000005, 0, f0};
//+
Point(162) = {0.1728, 0.31360000000000005, 0, f0};
//+
Point(163) = {0.1664, 0.31360000000000005, 0, f0};
//+
Point(164) = {0.16, 0.31360000000000005, 0, f0};
//+
Point(165) = {0.15360000000000001, 0.31360000000000005, 0, f0};
//+
Point(166) = {0.1472, 0.31360000000000005, 0, f0};
//+
Point(167) = {0.1408, 0.31360000000000005, 0, f0};
//+
Point(168) = {0.13440000000000002, 0.31360000000000005, 0, f0};
//+
Point(169) = {0.128, 0.31360000000000005, 0, f0};
//+
Point(170) = {0.1216, 0.30720000000000003, 0, f0};
//+
Point(171) = {0.11520000000000001, 0.3008, 0, f0};
//+
Point(172) = {0.10880000000000001, 0.2944, 0, f0};
//+
Point(173) = {0.1024, 0.28800000000000003, 0, f0};
//+
Point(174) = {0.09600000000000002, 0.2816, 0, f0};
//+
Point(175) = {0.08960000000000001, 0.27520000000000006, 0, f0};
//+
Point(176) = {0.0832, 0.26880000000000004, 0, f0};
//+
Point(177) = {0.07680000000000001, 0.2624, 0, f0};
//+
Point(178) = {0.0704, 0.256, 0, f0};
//+
Point(179) = {0.064, 0.24960000000000002, 0, f0};
//+
Point(180) = {0.057600000000000005, 0.2432, 0, f0};
//+
Point(181) = {0.0512, 0.23680000000000004, 0, f0};
//+
Point(182) = {0.044800000000000006, 0.23040000000000002, 0, f0};
//+
Point(183) = {0.038400000000000004, 0.22400000000000003, 0, f0};
//+
Point(184) = {0.032, 0.21760000000000002, 0, f0};
//+
Point(185) = {0.0256, 0.2112, 0, f0};
//+
Point(186) = {0.019200000000000002, 0.2048, 0, f0};
//+
Point(187) = {0.0128, 0.1984, 0, f0};
//+
Point(188) = {0.0064, 0.19200000000000003, 0, f0};
//+
Point(189) = {0.0, 0.18560000000000001, 0, f0};
//+
Point(190) = {-0.0064, 0.17920000000000003, 0, f0};
//+
Point(191) = {-0.0128, 0.1728, 0, f0};
//+
Point(192) = {-0.019200000000000002, 0.1664, 0, f0};
//+
Point(193) = {-0.0256, 0.16, 0, f0};
//+
Point(194) = {-0.032, 0.15360000000000001, 0, f0};
//+
Point(195) = {-0.038400000000000004, 0.1472, 0, f0};
//+
Point(196) = {-0.044800000000000006, 0.1408, 0, f0};
//+
Point(197) = {-0.0512, 0.13440000000000002, 0, f0};
//+
Point(198) = {-0.057600000000000005, 0.128, 0, f0};
//+
Point(199) = {-0.064, 0.1216, 0, f0};
//+
Point(200) = {-0.0704, 0.11520000000000001, 0, f0};
//+
Point(201) = {-0.07680000000000001, 0.10880000000000001, 0, f0};
//+
Point(202) = {-0.0832, 0.1024, 0, f0};
//+
Point(203) = {-0.08960000000000001, 0.09600000000000002, 0, f0};
//+
Point(204) = {-0.09600000000000002, 0.08960000000000001, 0, f0};
//+
Point(205) = {-0.09600000000000002, 0.0832, 0, f0};
//+
Point(206) = {-0.09600000000000002, 0.07680000000000001, 0, f0};
//+
Point(207) = {-0.09600000000000002, 0.0704, 0, f0};
//+
Point(208) = {-0.09600000000000002, 0.064, 0, f0};
//+
Point(209) = {-0.09600000000000002, 0.057600000000000005, 0, f0};
//+
Point(210) = {-0.09600000000000002, 0.0512, 0, f0};
//+
Point(211) = {-0.09600000000000002, 0.044800000000000006, 0, f0};
//+
Point(212) = {-0.09600000000000002, 0.038400000000000004, 0, f0};
//+
Point(213) = {-0.09600000000000002, 0.032, 0, f0};
//+
Point(214) = {-0.09600000000000002, 0.0256, 0, f0};
//+
Point(215) = {-0.09600000000000002, 0.019200000000000002, 0, f0};
//+
Point(216) = {-0.09600000000000002, 0.0128, 0, f0};
//+
Point(217) = {-0.09600000000000002, 0.0064, 0, f0};
//+
Line(5) = {2, 6};
//+
Line(6) = {6, 7};
//+
Line(7) = {7, 8};
//+
Line(8) = {8, 9};
//+
Line(9) = {9, 10};
//+
Line(10) = {10, 11};
//+
Line(11) = {11, 12};
//+
Line(12) = {12, 13};
//+
Line(13) = {13, 14};
//+
Line(14) = {14, 15};
//+
Line(15) = {15, 16};
//+
Line(16) = {16, 17};
//+
Line(17) = {17, 18};
//+
Line(18) = {18, 19};
//+
Line(19) = {19, 20};
//+
Line(20) = {20, 21};
//+
Line(21) = {21, 22};
//+
Line(22) = {22, 23};
//+
Line(23) = {23, 24};
//+
Line(24) = {24, 25};
//+
Line(25) = {25, 26};
//+
Line(26) = {26, 27};
//+
Line(27) = {27, 28};
//+
Line(28) = {28, 29};
//+
Line(29) = {29, 30};
//+
Line(30) = {30, 31};
//+
Line(31) = {31, 32};
//+
Line(32) = {32, 33};
//+
Line(33) = {33, 34};
//+
Line(34) = {34, 35};
//+
Line(35) = {35, 36};
//+
Line(36) = {36, 37};
//+
Line(37) = {37, 38};
//+
Line(38) = {38, 39};
//+
Line(39) = {39, 40};
//+
Line(40) = {40, 41};
//+
Line(41) = {41, 42};
//+
Line(42) = {42, 43};
//+
Line(43) = {43, 44};
//+
Line(44) = {44, 45};
//+
Line(45) = {45, 46};
//+
Line(46) = {46, 47};
//+
Line(47) = {47, 48};
//+
Line(48) = {48, 49};
//+
Line(49) = {49, 50};
//+
Line(50) = {50, 51};
//+
Line(51) = {51, 52};
//+
Line(52) = {52, 53};
//+
Line(53) = {53, 54};
//+
Line(54) = {54, 55};
//+
Line(55) = {55, 56};
//+
Line(56) = {56, 57};
//+
Line(57) = {57, 58};
//+
Line(58) = {58, 59};
//+
Line(59) = {59, 60};
//+
Line(60) = {60, 61};
//+
Line(61) = {61, 62};
//+
Line(62) = {62, 63};
//+
Line(63) = {63, 64};
//+
Line(64) = {64, 65};
//+
Line(65) = {65, 66};
//+
Line(66) = {66, 67};
//+
Line(67) = {67, 68};
//+
Line(68) = {68, 69};
//+
Line(69) = {69, 70};
//+
Line(70) = {70, 71};
//+
Line(71) = {71, 72};
//+
Line(72) = {72, 73};
//+
Line(73) = {73, 74};
//+
Line(74) = {74, 75};
//+
Line(75) = {75, 76};
//+
Line(76) = {76, 77};
//+
Line(77) = {77, 78};
//+
Line(78) = {78, 79};
//+
Line(79) = {79, 80};
//+
Line(80) = {80, 81};
//+
Line(81) = {81, 82};
//+
Line(82) = {82, 83};
//+
Line(83) = {83, 84};
//+
Line(84) = {84, 85};
//+
Line(85) = {85, 86};
//+
Line(86) = {86, 87};
//+
Line(87) = {87, 88};
//+
Line(88) = {88, 89};
//+
Line(89) = {89, 90};
//+
Line(90) = {90, 91};
//+
Line(91) = {91, 92};
//+
Line(92) = {92, 93};
//+
Line(93) = {93, 94};
//+
Line(94) = {94, 95};
//+
Line(95) = {95, 96};
//+
Line(96) = {96, 97};
//+
Line(97) = {97, 98};
//+
Line(98) = {98, 99};
//+
Line(99) = {99, 100};
//+
Line(100) = {100, 101};
//+
Line(101) = {101, 102};
//+
Line(102) = {102, 103};
//+
Line(103) = {103, 104};
//+
Line(104) = {104, 105};
//+
Line(105) = {105, 106};
//+
Line(106) = {106, 107};
//+
Line(107) = {107, 108};
//+
Line(108) = {108, 109};
//+
Line(109) = {109, 110};
//+
Line(110) = {110, 111};
//+
Line(111) = {111, 112};
//+
Line(112) = {112, 113};
//+
Line(113) = {113, 114};
//+
Line(114) = {114, 115};
//+
Line(115) = {115, 116};
//+
Line(116) = {116, 117};
//+
Line(117) = {117, 118};
//+
Line(118) = {118, 119};
//+
Line(119) = {119, 120};
//+
Line(120) = {120, 121};
//+
Line(121) = {121, 122};
//+
Line(122) = {122, 123};
//+
Line(123) = {123, 124};
//+
Line(124) = {124, 125};
//+
Line(125) = {125, 126};
//+
Line(126) = {126, 127};
//+
Line(127) = {127, 128};
//+
Line(128) = {128, 129};
//+
Line(129) = {129, 130};
//+
Line(130) = {130, 131};
//+
Line(131) = {131, 132};
//+
Line(132) = {132, 133};
//+
Line(133) = {133, 134};
//+
Line(134) = {134, 135};
//+
Line(135) = {135, 136};
//+
Line(136) = {136, 137};
//+
Line(137) = {137, 138};
//+
Line(138) = {138, 139};
//+
Line(139) = {139, 140};
//+
Line(140) = {140, 141};
//+
Line(141) = {141, 142};
//+
Line(142) = {142, 143};
//+
Line(143) = {143, 144};
//+
Line(144) = {144, 145};
//+
Line(145) = {145, 146};
//+
Line(146) = {146, 147};
//+
Line(147) = {147, 148};
//+
Line(148) = {148, 149};
//+
Line(149) = {149, 150};
//+
Line(150) = {150, 151};
//+
Line(151) = {151, 152};
//+
Line(152) = {152, 153};
//+
Line(153) = {153, 154};
//+
Line(154) = {154, 155};
//+
Line(155) = {155, 156};
//+
Line(156) = {156, 157};
//+
Line(157) = {157, 158};
//+
Line(158) = {158, 159};
//+
Line(159) = {159, 160};
//+
Line(160) = {160, 161};
//+
Line(161) = {161, 162};
//+
Line(162) = {162, 163};
//+
Line(163) = {163, 164};
//+
Line(164) = {164, 165};
//+
Line(165) = {165, 166};
//+
Line(166) = {166, 167};
//+
Line(167) = {167, 168};
//+
Line(168) = {168, 169};
//+
Line(169) = {169, 170};
//+
Line(170) = {170, 171};
//+
Line(171) = {171, 172};
//+
Line(172) = {172, 173};
//+
Line(173) = {173, 174};
//+
Line(174) = {174, 175};
//+
Line(175) = {175, 176};
//+
Line(176) = {176, 177};
//+
Line(177) = {177, 178};
//+
Line(178) = {178, 179};
//+
Line(179) = {179, 180};
//+
Line(180) = {180, 181};
//+
Line(181) = {181, 182};
//+
Line(182) = {182, 183};
//+
Line(183) = {183, 184};
//+
Line(184) = {184, 185};
//+
Line(185) = {185, 186};
//+
Line(186) = {186, 187};
//+
Line(187) = {187, 188};
//+
Line(188) = {188, 189};
//+
Line(189) = {189, 190};
//+
Line(190) = {190, 191};
//+
Line(191) = {191, 192};
//+
Line(192) = {192, 193};
//+
Line(193) = {193, 194};
//+
Line(194) = {194, 195};
//+
Line(195) = {195, 196};
//+
Line(196) = {196, 197};
//+
Line(197) = {197, 198};
//+
Line(198) = {198, 199};
//+
Line(199) = {199, 200};
//+
Line(200) = {200, 201};
//+
Line(201) = {201, 202};
//+
Line(202) = {202, 203};
//+
Line(203) = {203, 204};
//+
Line(204) = {204, 205};
//+
Line(205) = {205, 206};
//+
Line(206) = {206, 207};
//+
Line(207) = {207, 208};
//+
Line(208) = {208, 209};
//+
Line(209) = {209, 210};
//+
Line(210) = {210, 211};
//+
Line(211) = {211, 212};
//+
Line(212) = {212, 213};
//+
Line(213) = {213, 214};
//+
Line(214) = {214, 215};
//+
Line(215) = {215, 216};
//+
Line(216) = {216, 217};
//+
Line(217) = {217, 1};
//+
Curve loop(1) = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217};
//+
Plane Surface(1)= {1};
//+
Physical Surface("1") = {1};
//+
Physical Curve("2") = {112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,217};
//+
Physical Curve("3") = {5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110};
//+
Physical Curve("4") = {111};