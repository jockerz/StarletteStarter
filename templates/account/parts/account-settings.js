window.addEventListener('DOMContentLoaded', function () {
  const image_input = document.getElementById('image_input');
  const img_preview = document.getElementById('img_preview');
  const btn_upload = document.getElementById('btn_upload');

  image_input.addEventListener('change', function(e) {
    var files = e.target.files;

    if (!files || files.length === 0) {
			return null;
    } else {
    	var done = function (url) {
				img_preview.src = url;
			}

			if (URL)
        done(URL.createObjectURL(files[0]));
      else if (FileReader) {
        reader = new FileReader();
        reader.onload = function (e) { done(reader.result); };
        reader.readAsDataURL(files[0]);
      }
    }

    cropper = new Cropper(img_preview, {
      aspectRatio: 1, viewMode: 3,
      minCanvasWidth: 250, minCanvasHeight: 250,
      minCropBoxWidth: 240, minCropBoxHeight: 240,
    });

    btn_upload.disabled = false;
		btn_upload.addEventListener('click', function() {
			const csrf = document.getElementById("csrf_token").value;
			const canvas = cropper.getCroppedCanvas({width: 250, height: 250});
			img_preview.src = canvas.toDataURL();

			canvas.toBlob(function (blob) {
				var formData = new FormData();
				formData.append('img', blob);
				formData.append('csrf_token', csrf);

				$.ajax("{{ url_for('account:update_photo') }}", {
					method: 'POST',
					data: formData,
					processData: false,
					contentType: false,

					success: function(resp) {
						Swal.fire({
							icon: 'success',
							title: 'Yayy..',
							text: "{{ _('Profile picture updated. Reloading...') }}",
						});
						location.reload();
					},

					error: function(result, status, error) {
						Swal.fire({
							icon: 'error',
							title: 'Oops...',
							text: "{{ _('Image upload failed. Please try again later.') }}",
						});
					},
				});
			});
		})
  });
});