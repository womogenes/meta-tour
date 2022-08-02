const deleteTour = async (tourID) => {
  document
    .querySelector(`#${tourID} .card-content button`)
    .classList.add('is-loading');
  let response = await fetch(`/delete-tour/${tourID}`, {
    method: 'POST',
  });

  console.info(response);

  if (response.status == 204) {
    document.querySelector(`#${tourID}`).remove();
  }
};
