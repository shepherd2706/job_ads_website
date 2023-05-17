function delete_ad(adId) {
  fetch("/delete-ad", {
    method: "POST",
    body: JSON.stringify({ adId: adId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}