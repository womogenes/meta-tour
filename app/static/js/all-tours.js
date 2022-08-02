const deleteTour = async (tourID) => {
  let response = await fetch(`/delete-tour/${tourID}`, {
    method: 'POST',
  });

  if (response.status == 204) {
    document.querySelector(`#tour-${tourID}`).parentElement.remove();
  }
};
