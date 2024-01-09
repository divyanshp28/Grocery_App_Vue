// Function to check if the user is logged in
export function checkLoggedIn() {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token');
  const role = localStorage.getItem('role') || sessionStorage.getItem('role');
  return !!token && !!role;
}

export function isLoggedIn(to, from, next) {
  if (checkLoggedIn()) {
    next();
  } else {
    window.alert('You need to log in to access the cart.');
    next('/login');
  }
}

// Function to check if the user is an admin
export function checkAdmin() {
  try {
    const role = localStorage.getItem('role') || sessionStorage.getItem('role');
    return role === 'admin';
  } catch (error) {
    console.error('If you are admin, please login using your admin credentials', error);
    return false;
  }
}

export function isAdmin(to, from, next) {
  if (checkAdmin()) {
    
    next();
  } else {
    window.alert('Your are not allowed to access this resource. If you are the admin, login with your admin credentials.')
    next('/login'); 
  }
}


// Function to check if user is store admin

export function checkStoreAdmin() {
  try {
    const role = localStorage.getItem('role') || sessionStorage.getItem('role');
    return role === 'store_admin';
  } catch (error) {
    console.error('If you are store admin, please login using your store admin credentials', error);
    return false;
  }
}

export function isStoreAdmin(to, from, next) {
  if (checkStoreAdmin()) {
    
    next();
  } else {
    window.alert('Your are not allowed to access this resource. If you are the store admin, login with your admin credentials.')
    next('/login'); 
  }
}
