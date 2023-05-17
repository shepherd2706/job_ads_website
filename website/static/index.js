function delete_job(jobId) {
  fetch("/delete-job", {
    method: "POST",
    body: JSON.stringify({ jobId: jobId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}