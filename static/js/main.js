// TecnoCar - Main JS
window.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('sidebarToggle');
    if (toggle) {
        toggle.addEventListener('click', e => {
            e.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
    if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        document.body.classList.add('sb-sidenav-toggled');
    }

    // Auto-dismiss alerts
    setTimeout(() => {
        document.querySelectorAll('.alert-dismissible').forEach(el => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
            bsAlert.close();
        });
    }, 4000);
});
