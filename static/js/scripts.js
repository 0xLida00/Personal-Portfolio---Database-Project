$(document).ready(function () {
    // Edit Experience Modal
    $('#editExperienceModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var experienceId = button.data('experience-id');
        var position = button.data('position');
        var company = button.data('company');
        var startDate = button.data('start-date');
        var endDate = button.data('end-date') || '';  // Optional end date
        var description = button.data('description');
        
        var modal = $(this);
        
        modal.find('#edit_experience_id').val(experienceId);
        modal.find('#edit_position').val(position);
        modal.find('#edit_company').val(company);
        modal.find('#edit_start_date').val(startDate);
        modal.find('#edit_end_date').val(endDate);
        modal.find('#edit_description').val(description);
        
        modal.find('#editExperienceForm').attr('action', '/edit_experience/' + experienceId);
    });

    // Delete Experience Modal
    $('#deleteExperienceModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var experienceId = button.data('experience-id');
        var experienceName = button.data('experience-name');

        var modal = $(this);
        modal.find('#deleteConfirmMessage').text(`Are you sure you want to delete the experience: "${experienceName}"?`);

        var formAction = '/delete_experience/' + experienceId;

        modal.find('#deleteConfirmButton').off('click').on('click', function () {
            var form = $('<form>', {
                'action': formAction,
                'method': 'POST'
            });
            $('body').append(form);
            form.submit();
        });
    });

    // Skill Management Modal
    $('#editSkillModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var skillId = button.data('skill-id');
        var skillName = button.data('skill-name');
        var proficiencyLevel = button.data('proficiency-level');
        var category = button.data('category');
        var active = button.data('active');
    
        var modal = $(this);
        modal.find('#edit_skill_id').val(skillId);
        modal.find('#edit_skill_name').val(skillName);
        modal.find('#edit_proficiency_level').val(proficiencyLevel);
        modal.find('#edit_category').val(category);
        modal.find('#edit_active').val(active ? 'True' : 'False');
    });

    // Delete Skill Modal
    window.confirmDeleteSkill = function(skillId, skillName) {
        var confirmMessage = `Are you sure you want to delete the skill "${skillName}"?`;
        $('#confirmMessage').text(confirmMessage);
        $('#confirmButton').off('click').on('click', function() {
            window.location.href = `/delete_skill/${skillId}`;
        });
        $('#confirmModal').modal('show');
    };

    // Project Management: Edit Project Modal
    $('#editProjectModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var projectId = button.data('project-id');
        var title = button.data('title');
        var description = button.data('description');
        var technologies = button.data('technologies');
        var link = button.data('link');
        var modal = $(this);

        modal.find('#edit_project_id').val(projectId);
        modal.find('#edit_title').val(title);
        modal.find('#edit_description').val(description);
        modal.find('#edit_technologies').val(technologies);
        modal.find('#edit_link').val(link);
        modal.find('#editProjectForm').attr('action', '/edit_project/' + projectId);
    });

    // Confirm Delete Project
    window.confirmDeleteProject = function (projectId, projectTitle) {
        $('#deleteConfirmMessage').text(`Are you sure you want to delete the project "${projectTitle}"?`);
        $('#deleteConfirmButton')
            .off('click')
            .on('click', function () {
                window.location.href = `/delete_project/${projectId}`;
            });
        $('#confirmDeleteModal').modal('show');
    };

    // Password Validation
    const validatePassword = () => {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        const submitButton = document.getElementById('registerBtn');

        // Check if the passwords match
        if (password !== confirmPassword) {
            document.querySelector('.invalid-feedback').style.display = 'block';
            submitButton.disabled = true;
            return false;
        } else {
            document.querySelector('.invalid-feedback').style.display = 'none';
            submitButton.disabled = false;
            return true;
        }
    };

    document.getElementById('password').addEventListener('input', validatePassword);
    document.getElementById('confirm_password').addEventListener('input', validatePassword);

    // Prevent form submission if validation fails
    $('form[action*="register"]').on('submit', function (e) {
        if (!validatePassword()) {
            e.preventDefault();
        }
    });
});