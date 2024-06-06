document.querySelectorAll('#link').forEach(anchor => {
    anchor.addEventListener('click', function (event) {
        event.preventDefault(); // Empêche le comportement par défaut du lien

        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

  // Fonction pour rediriger l'utilisateur vers le tableau de bord sélectionné
  function navigateToDashboard(select) {
    const selectedOption = select.value;
    if (selectedOption) {
      window.location.href = selectedOption;
    }
  }

