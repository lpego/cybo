<?php
/*
Template Name: User Abstracts
*/
get_header();

global $wpdb;

// Get the current username from the URL.
$username = get_query_var('username');
if ($username) {
    // Query user data from wp_users and wp_usermeta.
    $user = $wpdb->get_row($wpdb->prepare("
        SELECT u.ID, u.user_login 
        FROM {$wpdb->users} u 
        WHERE u.user_login = %s
    ", $username));

    if ($user) {
        // Get the info from meta fields.
        $abstract_title = get_user_meta($user->ID, 'user_registration_textarea_1731322981011', true);
        $abstract_text = get_user_meta($user->ID, 'user_registration_textarea_1728640476', true);
        $first_name = get_user_meta($user->ID, 'first_name', true);
        $last_name = get_user_meta($user->ID, 'last_name', true);
        $author_role = get_user_meta($user->ID, 'user_registration_radio_1728638787', true);
        $author_affiliation = get_user_meta($user->ID, 'user_registration_input_box_1623050696', true);
        $contribution_type = get_user_meta($user->ID, 'user_registration_radio_1728639124', true);
        $preferred_session = get_user_meta($user->ID, 'user_registration_select_1731329777', true);
        $alternative_session = get_user_meta($user->ID, 'user_registration_select_1731330026149', true);
        $other_author1 = get_user_meta($user->ID, 'user_registration_input_box_1623053158710', true);
        $other_author2 = get_user_meta($user->ID, 'user_registration_input_box_1731330537529', true);
        $other_author3 = get_user_meta($user->ID, 'user_registration_input_box_1731330538041', true);
        $other_author4 = get_user_meta($user->ID, 'user_registration_input_box_1731330538340', true);
        $other_author5 = get_user_meta($user->ID, 'user_registration_input_box_1731330538474', true);
        $other_author6 = get_user_meta($user->ID, 'user_registration_input_box_1731330538610', true);
        $other_author7 = get_user_meta($user->ID, 'user_registration_input_box_1731330538743', true);
        $other_author8 = get_user_meta($user->ID, 'user_registration_input_box_1731330538896', true);
        $other_author9 = get_user_meta($user->ID, 'user_registration_input_box_1731330539036', true);
        $other_author_affiliation1 = get_user_meta($user->ID, 'user_registration_input_box_1623052381811', true);
        $other_author_affiliation2 = get_user_meta($user->ID, 'user_registration_input_box_1623053192355', true);
        $other_author_affiliation3 = get_user_meta($user->ID, 'user_registration_input_box_1731319907155', true);
        $other_author_affiliation4 = get_user_meta($user->ID, 'user_registration_input_box_1731319907299', true);
        $other_author_affiliation5 = get_user_meta($user->ID, 'user_registration_input_box_1731319907446', true);
        $other_author_affiliation6 = get_user_meta($user->ID, 'user_registration_input_box_1731319907598', true);
        $other_author_affiliation7 = get_user_meta($user->ID, 'user_registration_input_box_1731319907738', true);
        $other_author_affiliation8 = get_user_meta($user->ID, 'user_registration_input_box_1731320292178', true);
        $other_author_affiliation9 = get_user_meta($user->ID, 'user_registration_input_box_1731320292481', true);

        if ($abstract_title) {
            echo '<h2>' . esc_html($abstract_title) . '</h2>';
            // echo '<h3>' . esc_html($first_name) . ' ' . esc_html($last_name) . '<sup>1</sup></h3>';

            // Initialize arrays for authors and affiliations
            $authors = [];
            $authors_affiliations = [];

            // Add the main author
            $authors[] = esc_html($first_name . ' ' . $last_name);
            $authors_affiliations[] = esc_html($author_affiliation);

            // Define other authors and their affiliations
            $other_authors = [
                $other_author1, $other_author2, $other_author3, $other_author4, 
                $other_author5, $other_author6, $other_author7, $other_author8, $other_author9
            ];
            $other_affiliations = [
                $other_author_affiliation1, $other_author_affiliation2, $other_author_affiliation3, 
                $other_author_affiliation4, $other_author_affiliation5, $other_author_affiliation6, 
                $other_author_affiliation7, $other_author_affiliation8, $other_author_affiliation9
            ];

            // Add other authors and affiliations to the arrays
            foreach ($other_authors as $index => $author) {
                if ($author) {
                    $authors[] = esc_html($author);
                    $authors_affiliations[] = esc_html($other_affiliations[$index]);
                }
            }

            // Now we need to ensure that authors with the same affiliation get the same superscript
            $unique_affiliations = [];
            $affiliation_to_superscript = [];
            $affiliation_to_authors = [];

            // Assign superscript numbers based on affiliations
            foreach ($authors_affiliations as $index => $affiliation) {
                if (!in_array($affiliation, $unique_affiliations)) {
                    $superscript = count($unique_affiliations) + 1; // Increment superscript number
                    $unique_affiliations[] = $affiliation;
                    $affiliation_to_superscript[$affiliation] = $superscript;
                    $affiliation_to_authors[$affiliation] = [$authors[$index]];
                } else {
                    $affiliation_to_authors[$affiliation][] = $authors[$index];
                }
            }

            // Output authors on one line with superscripts
            $author_line = [];
            foreach ($authors_affiliations as $index => $affiliation) {
                $superscript = $affiliation_to_superscript[$affiliation];
                $author_line[] = $authors[$index] . ' <sup>' . $superscript . '</sup>';
            }

            echo '<h4>' . implode(', ', $author_line) . '</h4>';

            // Output affiliations on a separate line, each printed only once
            $affiliation_line = [];
            foreach ($unique_affiliations as $affiliation) {
                $superscript = $affiliation_to_superscript[$affiliation];
                $affiliation_line[] = $affiliation . ' <sup>' . $superscript . '</sup>';
            }

            echo '<h4>' . implode(', ', $affiliation_line) . '</h4>';

            // Output the abstract text
            echo '<p>' . esc_html($abstract_text) . '</p>';

            // Output other useful info
            echo '<p> <strong>Main author career stage: </strong>' . esc_html($author_role) . '</p>';
            echo '<p> <strong>Contribution type: </strong>' . esc_html($contribution_type) . '</p>';
            echo '<p> <strong>First choice session: </strong>' . esc_html($preferred_session) . '</p>';
            echo '<p> <strong>Second choice session: </strong>' . esc_html($alternative_session) . '</p>';


        } else {
            echo '<p>No abstract title found for this user.</p>';
        }
    } else {
        echo '<p>User not found.</p>';
    }
} else {
    echo '<p>No user specified.</p>';
}

get_footer();
?>
