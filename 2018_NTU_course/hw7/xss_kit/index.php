<!DOCTYPE html>
<html lang="en" class="no-js">

<head>
	<meta charset="UTF-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>XSS Kitchen</title>
	<meta name="description" content="Blueprint: A basic template for a responsive multi-level menu" />
	<meta name="keywords" content="blueprint, template, html, css, menu, responsive, mobile-friendly" />
	<meta name="author" content="Codrops" />
	<link rel="shortcut icon" href="favicon.ico">
	<!-- food icons -->
	<link rel="stylesheet" type="text/css" href="css/organicfoodicons.css" />
	<!-- demo styles -->
	<link rel="stylesheet" type="text/css" href="css/demo.css" />
	<!-- menu styles -->
	<link rel="stylesheet" type="text/css" href="css/component.css" />
    <script src="js/modernizr-custom.js"></script>
    <style>
    th {
        padding-top: 11px;
        padding-bottom: 11px;
    }

    code {
        color: #e83e8c;
        background-color: white;
        border-radius: 2px;
        padding: 3px;
        margin: 5px;
    }

    .button {
        background-color: #008CBA;
        border: none;
        border-radius: 4px;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
    }

    .button:hover {
        box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
    }

    </style>
</head>

<body>
	<!-- Main container -->
	<div class="container">
		<!-- Blueprint header -->
		<header class="bp-header cf">
			<div class="dummy-logo">
				<div class="dummy-icon foodicon foodicon--coconut"></div>
				<h2 class="dummy-heading">XSS Kitchen</h2>
			</div>
        </header>
		<button class="action action--open" aria-label="Open Menu"><span class="icon icon--menu"></span></button>
		<nav id="ml-menu" class="menu">
			<button class="action action--close" aria-label="Close Menu"><span class="icon icon--cross"></span></button>
			<div class="menu__wrap">
				<ul data-menu="main" class="menu__level" tabindex="-1" role="menu" aria-label="All">
					<li class="menu__item" role="menuitem"><a class="menu__link" data-submenu="submenu-1" href="#">Challenge</a></li>
                    <li class="menu__item" role="menuitem"><a class="menu__link" data-submenu="submenu-2" href="#">Rank</a></li>
                    					<li class="menu__item" role="menuitem"><a class="menu__link" data-submenu="submenu-3" href="#">Register</a></li>
                    <li class="menu__item" role="menuitem"><a class="menu__link" data-submenu="submenu-4" href="#">Login</a></li>
                    					<li class="menu__item" role="menuitem"><a class="menu__link" data-submenu="submenu-4" href="#">Help</a></li>
				</ul>
            </div>
		</nav>
		<div class="content">
            <p class="info">Welcome to the XSS kitchen</p>			<!-- Ajax loaded content here -->
		</div>
	</div>
	<!-- /view -->
	<script src="js/classie.js"></script>
	<script src="js/dummydata.js"></script>
	<script src="js/main.js"></script>
	<script>
	(function() {
		var menuEl = document.getElementById('ml-menu'),
			mlmenu = new MLMenu(menuEl, {
				// breadcrumbsCtrl : true, // show breadcrumbs
				// initialBreadcrumb : 'all', // initial breadcrumb text
				backCtrl : false, // show back button
				// itemsDelayInterval : 60, // delay between each menu item sliding animation
				onItemClick: loadDummyData // callback: item that doesn´t have a submenu gets clicked - onItemClick([event], [inner HTML of the clicked item])
			});

		// mobile menu toggle
		var openMenuCtrl = document.querySelector('.action--open'),
			closeMenuCtrl = document.querySelector('.action--close');

		openMenuCtrl.addEventListener('click', openMenu);
		closeMenuCtrl.addEventListener('click', closeMenu);

		function openMenu() {
			classie.add(menuEl, 'menu--open');
			closeMenuCtrl.focus();
		}

		function closeMenu() {
			classie.remove(menuEl, 'menu--open');
			openMenuCtrl.focus();
		}

		// simulate grid content loading
		var gridWrapper = document.querySelector('.content');

		function loadDummyData(ev, itemName) {
			ev.preventDefault();

			closeMenu();
			gridWrapper.innerHTML = '';
			classie.add(gridWrapper, 'content--loading');
			setTimeout(function() {
				classie.remove(gridWrapper, 'content--loading');
                //gridWrapper.innerHTML = '<ul class="products">' + dummyData[itemName] + '<ul>';
                if(itemName == 'Challenge') 
                    gridWrapper.innerHTML = '<p class="info">Login First!</p>' +                        '<ul>';
                else if(itemName == 'Rank')
                    gridWrapper.innerHTML = '<ul class="products">' + '<p class="info">Login First!</p>'+'<ul>';                else if(itemName == 'Help')
                    gridWrapper.innerHTML = '<ul class="products">' + '<h1>特級廚師的考驗</h1><br><p>共有10道料理，每道料理代表一種場景</p><p>每組食材代表一種輸入</p><p>只要能成功<code>alert()</code>就算完成料理!</p><br><p>用一組食材同時完成10道料理且長度小於110，即可獲得FLAG!</p><br>' + 
                    '<p>舉例:</p>' + 
                    '料理1: <code>&lt;!--[食材]--&gt;</code> <br>'+
                    '料理2: <code>&lt;div&gt;[食材]&lt;/div&gt;</code> <br>'+
                    '欲同時完成這兩道料理，可以輸入食材:  <code>--&gt;&lt;svg/onload=alert()&gt;</code>' +
                    '<ul>';
                else if(itemName == 'Logout')
                    window.location="index.php?action=logout";
                else if(itemName == 'Login')
                    gridWrapper.innerHTML = '<ul class="products">' + 
                    '<form method="post">' +
                    '<input type="text" name="l_user" style="height:50px;width:30%" placeholder="Username"><br>' +
                    '<input type="password" name="l_pass" style="height:50px;width:30%; margin:10px" placeholder="Password"><br>' +
                    '<input type="hidden" name="action" value="login">' +
                    '<input class="button" type="submit" value="登入">' +
                    '</form>' + 
                    '<ul>';
                else if(itemName == 'Register') 
                    gridWrapper.innerHTML = '<ul class="products">' + 
                    '<form method="post">' + 
                    '<input type="text" name="user" style="height:50px;width:30%" placeholder="Username"><br>' +
                    '<input type="password" name="pass" style="height:50px; width:30%; margin:10px" placeholder="Password" ><br>' +
                    '<input type="hidden" name="action" value="register" >' +
                    '<input class="button" type="submit" value="註冊">' +
                    '</form>' +
                    '<ul>';
                else
                    gridWrapper.innerHTML = '<ul class="products">' + 'test' + '<ul>';
			}, 700);
		}
	})();
	</script>
</body>

</html>
