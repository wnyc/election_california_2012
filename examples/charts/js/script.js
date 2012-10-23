var config;

$(document).ready(function(){
    var statewide_contest_template = Handlebars.compile($("#statewide-contest-template").html());
    var district_contest_template = Handlebars.compile($("#district-contest-template").html());
    var county_results_template = Handlebars.compile($("#county-results-template").html());
    var result_row_template = Handlebars.compile($("#result-row-template").html());
    var result_table_template = Handlebars.compile($("#result-table-template").html());
    var proposition_results_template = Handlebars.compile($("#proposition-results-template").html());
    var election;
    var router;
    var REP_HI = "#f40b0b", REP_MED = "#ff6666", REP_LO = "#ffb0b0", DEM_HI = "#b6ecff", DEM_MED = "#6cceff", DEM_LO = "#009eff";
    
    var presidential_view, ussenate_view, ushouse_view, casenate_view, caassembly_view, propositions_view;
    var county_map_view, assembly_map_view, ushouse_map_view, casenate_map_view;
    Handlebars.registerHelper('result_table_template', result_table_template);
    Handlebars.registerHelper('county_results_template', county_results_template);
    Handlebars.registerHelper('add_commas', addCommas);

    function addCommas(nStr)
    {
        // Public domain code from http://www.mredkj.com/javascript/nfbasic.html
        nStr += '';
        x = nStr.split('.');
        x1 = x[0];
        x2 = x.length > 1 ? '.' + x[1] : '';
        var rgx = /(\d+)(\d{3})/;
        while (rgx.test(x1)) {
            x1 = x1.replace(rgx, '$1' + ',' + '$2');
        }
        return x1 + x2;
    }
    var Config = Backbone.Model.extend({
        // body, contest, county
        
        codeAddress: function() {
              var address = $('#zoombox').val();
              var map = this.get("map");
              this.get("geocoder").geocode( { 'address': address}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                  map.setCenter(results[0].geometry.location);
                                    map.setZoom(7);
                                    marker = new google.maps.Marker({
                    map:map,
                    draggable:false,
                    animation: google.maps.Animation.DROP,
                    position: results[0].geometry.location
                  });
                } else {
                  alert("Couldn't relocate for the following reason: " + status);
                }
              });
        },
        redraw_features : function () {
            var cfg = this;
            var feature_sets = this.get("map_feature_sets");
            _.each(feature_sets, function(feature_set_name)
            {
                cfg.redraw_feature_set(feature_set_name);
            });
            
        },
        redraw_feature_set : function (feature_set_name) {
                var feature_set = this.get(feature_set_name);
                if (feature_set == "pending")
                {
                    return;
                }
                
                _.each(feature_set, function(feature)
                {
                    feature.redraw();

                });

        },

        defaults: {
            body : "",
            contest: "",
            county: "",
            showcounties: false,
            showassembly: false,
            showsenate: false,
            showushouse: false,
            map: typeof google != "undefined" ? new google.maps.Map(document.getElementById("map-canvas"), {
                center: new google.maps.LatLng(38.5, -121.5), // near Sacramento
                zoom: 5,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                styles: map_styles,
                scrollwheel: false,
                streetViewControl: false,
                mapTypeControl: false
            }) : null,
            geocoder : new google.maps.Geocoder(),
            map_feature_sets: []

        }


    });

    var Election = Backbone.Collection.extend({
        // last_updated
        model: Body,
        parse_bodies: function(bodies){
            var the_election = this;
            _.each(bodies, function(body, name)
            {
                var newbody = new Body({ name : name, title: body.title });
                the_election.add(newbody);
                newbody.parse_contests(body.contests);

            });

        }

    });

    var Body = Backbone.Model.extend({
        // Name - e.g. us.president
        // Contests
        //

        parse_contests : function(contests){
            var the_body = this;
            var the_contests = new Contests();

            _.each(contests, function (contest, name)
            {
                var newcontest = new Contest({
                    name: name,
                    body: the_body,
                    longname: contest.longname,
                    geo: contest.geo,
                    precincts_total: contest.precincts.total,
                    precincts_reporting: contest.precincts.reporting,
                    measure_number: +contest.measure_number,
                    precincts_reporting_percent: contest.precincts.reporting_percent
                });
                newcontest.parse_candidates(contest.candidates);
                if (_.has(contest, 'counties'))
                {
                    var counties = new Counties();
                    _.each(contest.counties, function (county, name)
                    {
                        var newcounty = new County({
                            name: name,
                            title: county.title,
                            geo: county.geo,
                            candidates: county_votes_to_candidates(county.votes, newcontest.get("candidates")),
                            precincts_total: county.precincts.total,
                            precincts_reporting: county.precincts.reporting,
                            precincts_reporting_percent: county.precincts.reporting_percent


                        });
                        counties.add(newcounty);



                    });
                    newcontest.set('counties', counties);
                }
                else
                {
                    newcontest.set('counties', null);
                }
                var candidates = newcontest.get("candidates");
                // Remove third-party candidates
                // Consolidating them as other

                if(_.isUndefined(contest.measure_number))
                {
                    candidates.remove(candidates.filter(function(cand){return cand.get("party") != 'Dem' && cand.get("party") != 'Rep' && cand.get("party") != '---';}));
                }
                the_contests.add(newcontest);
            });
            the_body.set("contests", the_contests);

        }

    });

    var Contest = Backbone.Model.extend({
        // Name 
        // Longname
        // Geo
        // Body
        // Candidates
        // Precincts_reporting
        // Precincts_total
        // Precincts_reporting_percent
        // measure_number
        parse_candidates : function(candidates){
            var the_contest = this;
            var the_candidates = new Candidates();
            _.each(candidates, function(candidate, id)
            {
                var new_candidate = new Candidate(candidate);
                the_candidates.add(candidate);

            });
            if(the_candidates.size() > 2)
            {
                // Add 'Other' sum for neither rep/dem
                // And discard individual third-party candidates
                // We could make exceptions if we hear of any important ones
                var other_candidate = create_other_candidate(the_candidates);
                if (other_candidate)
                {
                    the_candidates.add(other_candidate);
                }


                
            }
            

            the_contest.set('candidates', the_candidates);

        }
    });
    var Contests = Backbone.Collection.extend({
        model : Contest,
        comparator: function (contest) {
            return contest.get("measure_number");

        }

    });

    var County = Backbone.Model.extend({
        // id
        // title
        // geo
        // votes
        // Precincts_reporting
        // Precincts_total
        // Precincts_reporting_percent


    });

    var Counties = Backbone.Collection.extend({
        model : County
    });

    function create_other_candidate(candidates)
    {
            var other_candidate = 
                new Candidate({
                    name: "Other",
                    party: "---",
                    last_name: "",
                    ballot_name: "Other",
                    id: "other"
                });
            var total_votes = 0;
            var total_vote_percent = 0;
            candidates.each(function(candidate){
                var party = candidate.get("party");
                if(party != 'Dem' && party != 'Rep')
                {
                    total_votes += parseInt(candidate.get("votes"), 10);
                    total_vote_percent += parseFloat(candidate.get("vote_percent"));
                }
            });
            other_candidate.set({votes: total_votes, vote_percent: total_vote_percent.toFixed(1)});
            if(total_votes == 0)
            {
                return null;
            }
            return other_candidate;

    }
    function county_votes_to_candidates(votes, candidates)
    {
        var newcandidates = new Candidates(_.map(votes, function(vote, candidate_id)
        {
            var new_candidate = candidates.get(candidate_id).clone();
            new_candidate.set(vote); // Override vote data

            return new_candidate;

            

        }));

        if (newcandidates.size() > 2)
        {
            var othercandidate = create_other_candidate(newcandidates);
            if (othercandidate)
            {
                newcandidates.add(othercandidate);
            }
            return newcandidates.remove(candidates.filter(function(cand){return cand.get("party") != 'Dem' && cand.get("party") != 'Rep' && cand.get("party") != '---';}));
        }
        
        return newcandidates;


    }
    var Candidate = Backbone.Model.extend({
        // name
        // id
        // ballot_name
        // last_name
        // votes
        // party
        // vote_percent

    });

    var Candidates = Backbone.Collection.extend({
        model: Candidate,
        comparator: function(candidate)
        {
            // Sort them in decreasing order of vote percentage
            return -1 * candidate.get("vote_percent");

        }

    });

    var DistrictContestView = Backbone.View.extend({
        tagName: "div",
        id: "district-contest-results",
        base_render : function(view){
            var title = view.model.get("title");
            var district = config.get("contest") || 1;
            district = parseInt(district, 10);
            m = view.model;
            var contest = m.get("contests").find(function(c){return c.get("geo").district == district;});
            if(!_.isUndefined(contest))
            {
                var json = contest.toJSON();
                json.candidates = json.candidates.toJSON();
                json.body_title = title;


                $(this.el).html(district_contest_template(json));
            }
            else
            {
                // Do the right thing when there's no valid race
            }
            $('#chart-canvas').html($(this.el)); 

        }

    });

    var AssemblyContestView = DistrictContestView.extend({
        render: function(district)
        {
            this.base_render(this);
            assembly_map_view.render(district);

        }

    });
    var USHouseContestView = DistrictContestView.extend({
        render: function(district)
        {
            this.base_render(this);
            ushouse_map_view.render(district);

        }

    });
    var CASenateContestView = DistrictContestView.extend({
        render: function(district)
        {
            this.base_render(this);
            casenate_map_view.render(district);

        }

    });

        
        

        
    var StatewideContestView = Backbone.View.extend({
        tagName: "div",
        id: "statewide-contest-results",
        render: function(county_name) {
            var json = this.model.toJSON();
            json.body_title = json.body.get("title");
            json.candidates = json.candidates.toJSON(); // Need this as object too

            if(!_.isUndefined(county_name))
            {
                j = json;
                var county_results = json.counties.where({title: county_name});
                if (county_results.length > 0)
                {
                   json.county_results = county_results.pop().toJSON();
                   json.county_results.candidates = json.county_results.candidates.toJSON();
                }

            }

            $(this.el).html(statewide_contest_template(json));
            $('#chart-canvas').html($(this.el)); 
            county_map_view.render(county_name);
            return this;
        }
    });

    var PropositionsView = Backbone.View.extend({
        tagName: "div",
        id: "proposition-contest-results",
        render: function(county_name) {
            var json = {};
            json.body_title = this.model.get("title");
            json.propositions = this.model.get("contests").toJSON();
            _.each(json.propositions, function(proposition) {
                // Need to compute percentages too
                // Always two vote types: Yes and No
                proposition.candidates = proposition.candidates.toJSON();
                var total = proposition.candidates[0].votes + proposition.candidates[1].votes;
                proposition.candidates[0].vote_percent = (100 * proposition.candidates[0].votes / total).toFixed(2);
                proposition.candidates[1].vote_percent = (100 * proposition.candidates[1].votes / total).toFixed(2);
                

            });

            if(!_.isUndefined(county_name))
            {
            }
            console.log(json);

            $(this.el).html(proposition_results_template(json));
            $('#chart-canvas').html($(this.el));
            county_map_view.render(county_name);

            
            

        }

    });

    function county_responsive_unselected_opts () {

        if (!config.get("showcounties"))
        {
            return {visible: false, fillOpacity: 0, strokeWidth:0 };
        }
        if (config.get("body") == "ca.propositions")
        {
        

        }


        // Red blue map
        if (config.get("county"))
        {
            // If another county is selected
            return {fillColor: "#999", fillOpacity: 0.7, strokeWidth: 1,visible: true };
        }

        else
        {
            var body = config.get("body");
            var contest = election.find(function(b){return b.get("name") == body}).get("contests").first(); // Only one for these statewide offices
            var thecounty = this.id;
            var county = contest.get("counties").find(function(c){
                return c.get("title") == thecounty;
            });
            if (county.get("precincts_reporting_percent") < 10)
            {
                // Insufficent data -- color it grey
                return {fillColor: "#999", fillOpacity: 0.7, strokeWidth: 1,visible: true };
            }


            var dem = county.get("candidates").find(function(c){return c.get("party") == "Dem"});
            var rep = county.get("candidates").find(function(c){return c.get("party") == "Rep"});

            if (_.isUndefined(dem))
            {
                dem_percent = 0;
            }
            else
            {
                dem_percent = dem.get("vote_percent");
            }
            if (_.isUndefined(rep))
            {
                rep_percent = 0;
            }
            else
            {
                rep_percent = rep.get("vote_percent");
            }

            if (rep_percent > 80)
            {
                return {fillColor: REP_HI, fillOpacity: 0.7, strokeWidth: 1,visible: true };
            }
            else if (rep_percent > 60)
            {
                return {fillColor: REP_MED, fillOpacity: 0.7, strokeWidth: 1,visible: true };
            }
            else if (rep_percent > 50)
            {
                return {fillColor: REP_LO, fillOpacity: 0.7, strokeWidth: 1,visible: true };
            }

            else if (dem_percent > 80)
            {
                return {fillColor: DEM_HI, fillOpacity: 0.7, strokeWidth: 1,visible: true };
            }
            else if (dem_percent > 60)
            {
                return {fillColor: DEM_MED, fillOpacity: 0.7, strokeWidth: 1,visible: true };
            }
            else if (dem_percent > 50)
            {
                return {fillColor: DEM_LO, fillOpacity: 0.7, strokeWidth: 1,visible: true };
            }
            else
            {
                return {fillColor: "#999", fillOpacity: 0.7, strokeWidth: 1,visible: true };
            }






                

            

        }



    }
    function county_responsive_highlighted_opts () {
        if (!config.get("showcounties"))
        {
            return {visible: false};
        }

        return {fillColor: "#ffcc33", fillOpacity: 0.7, visible: true};

    }
    function district_responsive_unselected_opts (poly, showflag) {
        if (!config.get(showflag))
        {
            return {visible: false, fillOpacity: 0, fillColor: "#ffffff"};
        }
        var body = config.get("body");
        var district_id = poly.id;
        e = election;
        contest = election.find(function(b){return b.get("name") == body}).get("contests").find(function(c){
            return c.get("geo").district == district_id;
        });

        if(_.isUndefined(contest))
        {
            // No contest in this district
            return {fillColor: "#999", fillOpacity: 0.7, visible: true};
        }

        var selected_district = config.get("contest");

        if (selected_district && selected_district != district_id)
        {
            return {fillColor: "#999", fillOpacity: 0.7, visible: true};

        }

        var dem = contest.get("candidates").find(function(c){return c.get("party") == "Dem"});
        var rep = contest.get("candidates").find(function(c){return c.get("party") == "Rep"});

        if (_.isUndefined(dem))
        {
            dem_percent = 0;
        }
        else
        {
            dem_percent = dem.get("vote_percent");
        }
        if (_.isUndefined(rep))
        {
            rep_percent = 0;
        }
        else
        {
            rep_percent = rep.get("vote_percent");
        }

        if (rep_percent > 80)
        {
            return {fillColor: REP_HI, fillOpacity: 0.7, strokeWidth: 1,visible: true };
        }
        else if (rep_percent > 60)
        {
            return {fillColor: REP_MED, fillOpacity: 0.7, strokeWidth: 1,visible: true };
        }
        else if (rep_percent > 50)
        {
            return {fillColor: REP_LO, fillOpacity: 0.7, strokeWidth: 1,visible: true };
        }

        else if (dem_percent > 80)
        {
            return {fillColor: DEM_HI, fillOpacity: 0.7, strokeWidth: 1,visible: true };
        }
        else if (dem_percent > 60)
        {
            return {fillColor: DEM_MED, fillOpacity: 0.7, strokeWidth: 1,visible: true };
        }
        else if (dem_percent > 50)
        {
            return {fillColor: DEM_LO, fillOpacity: 0.7, strokeWidth: 1,visible: true };
        }
        else
        {
            return {fillColor: "#999", fillOpacity: 0.7, strokeWidth: 1,visible: true };
        }





    }
    function district_responsive_highlighted_opts (poly, showflag) {

        
        if(!config.get(showflag))
        {
            return {visible: false};
        }
        return {fillColor: "#ffcc33", fillOpacity: 0.7, visible: true};

    }
    var DistrictMapView = Backbone.View.extend({
        tagname: "div",
        id: "the-map",
        render: function(district_id)
        {
            if (_.isNull(config.get("map")))
            {
                return;
            }
            if(!config.has(this.feature_name))
            {
                var idselector = this.idselector;
                var showflag = this.showflag;
                var feature_name = this.feature_name;
                config.set(feature_name, "pending");

                $.get(this.kml_url, function (data) {
                    var features = gmap.load_polygons({
                        map: config.get("map"),
                        data: data,
                        data_type: "kml",
                        idselector: idselector,
                        highlightCallback : function () {
                            var district = parseInt(this.id, 10);
                            config.set({contest: district});
                            config.redraw_feature_set(feature_name);


                        },
                        unhighlightCallback : function () {
                            config.set({contest: ''});
                            config.redraw_feature_set(feature_name);



                        },
                        responsive_unselected_opts: function(){return district_responsive_unselected_opts(this, showflag);},

                        responsive_highlighted_opts: function(){return district_responsive_highlighted_opts(this, showflag);}


                   });
                    config.set(feature_name, features, {silent: true});
                    var config_features = config.get("map_feature_sets");
                    config_features.push(feature_name);
                    config.set("map_feature_sets", config_features, {silent: true});

                });
             }
        }
    
    });

    var USHouseMapView = DistrictMapView.extend({
        feature_name: "house_features",
        kml_url: "kml/ca_congress_simple0020.kml",
        showflag: "showushouse",
        idselector: 'name',
        
        
    });

    var AssemblyMapView = DistrictMapView.extend({
        feature_name : "assembly_features",
        idselector: 'name',
        showflag: "showassembly",
        kml_url: "kml/ca_assembly_simple0020.kml"

    });
    
    var CASenateMapView = DistrictMapView.extend({
        feature_name : "senate_features",
        idselector: 'name',
        showflag: "showsenate",
        kml_url: "kml/ca_senate_simple0020.kml"

    });


    var CountyMapView = Backbone.View.extend({
        tagname: "div",
        id: "the-map",
        render: function(county_name)
        {
            if (_.isNull(config.get("map")))
            {
                return;
            }
            if(!config.has("county_features"))
            {
                var config_features = config.get("map_feature_sets");
                config_features.push("county_features");
                config.set("map_feature_sets", config_features, {silent: true});
                config.set("county_features", "pending");
               $.get("kml/california_counties_use_simplified.kml", function (data) {
                var features = gmap.load_polygons({
                    map: config.get("map"),
                    data: data,
                    data_type: "kml",
                    idselector: 'Data[name="NAME00"] value',
                    highlightCallback : function () {
                        var countyname = this.id;
                        config.set({county: countyname});
                        config.redraw_feature_set("county_features");


                    },
                    unhighlightCallback: function() {
                        config.set({county: ''});
                        config.redraw_feature_set("county_features");

                    },
                    responsive_unselected_opts: county_responsive_unselected_opts,

                    responsive_highlighted_opts: county_responsive_highlighted_opts


               });
                config.set("county_features", features, {silent: true});
                });
            

            }
        }

    });

    

    var Router = Backbone.Router.extend({
        routes : {
           "body/:body" : "navto",
           "body/:body/:contest" : "navto",
           "body/:body/:contest/" : "navto",
           "body/:body/:contest/:county/" : "navto",
           "body/:body/:contest/:county" : "navto"
        },
        navto: function(body, contest, county) {
            config.set({body : body || "us.president", contest: contest || '', county : county || '' }, {silent: true});
            this.show (body, contest, county);
        },

        show: function(body, contest, county) {
            if (body == "us.president")
            {
                presidential_view.render(county);
                config.set({
                    showcounties: true,
                    showassembly: false,
                    showsenate: false,
                    showushouse: false,
                    contest: '0'

                });

            }
            if (body == "us.senate")
            {
                ussenate_view.render(county);
                config.set({
                    showcounties: true,
                    showassembly: false,
                    showsenate: false,
                    showushouse: false,
                    contest: '0'

                });
            }
            else if (body == "us.house")
            {
                ushouse_view.render(contest);
                config.set({
                    showcounties: false,
                    showassembly: false,
                    showsenate: false,
                    showushouse: true,
                    county: ''

                });
            }
            else if (body == "ca.senate")
            {
                casenate_view.render(contest);
                config.set({
                    showcounties: false,
                    showassembly: false,
                    showsenate: true,
                    showushouse: false,
                    county: ''

                });
            }
            else if (body == "ca.assembly")
            {
                caassembly_view.render(contest);
                config.set({body : 'ca.assembly'});
                config.set({
                    showcounties: false,
                    showassembly: true,
                    showsenate: false,
                    showushouse: false,
                    county: ''

                });
            }
            else if (body == "ca.propositions")
            {
                propositions_view.render(county);
                config.set({
                    showcounties: true,
                    showassembly: false,
                    showsenate: false,
                    showushouse: false

                });
            }
            else {
                config.set({body : "us.president"});
                config.set({
                    showcounties: true,
                    showassembly: false,
                    showsenate: false,
                    showushouse: false

                });

            }
            $('.button').removeClass('button-selected');
            $('#' + body + '-button').addClass('button-selected');
            

        }

    });


    $.getJSON("data/foo.json", function(data)
    {
        election = new Election();
        election.parse_bodies(data.bodies);
        presidential_view = new StatewideContestView({model: election.where({name: 'us.president'}).pop().get("contests").first()});
        ussenate_view = new StatewideContestView({model: election.where({name: 'us.senate'}).pop().get("contests").first()});
        propositions_view = new PropositionsView({model: election.where({name: 'ca.propositions'}).pop()});

        caassembly_view = new AssemblyContestView({model: election.where({name: 'ca.assembly'}).pop()});
        casenate_view = new CASenateContestView({model: election.where({name: 'ca.senate'}).pop()});
        ushouse_view = new USHouseContestView({model: election.where({name: 'us.house'}).pop()});

        county_map_view = new CountyMapView();
        assembly_map_view = new AssemblyMapView();
        ushouse_map_view = new USHouseMapView();
        casenate_map_view = new CASenateMapView();
        router = new Router();
        config = new Config();

        config.on("change:contest change:county", function(){
            router.navigate("#body/" + config.get("body") + "/" + config.get("contest") + "/" + config.get("county"), {trigger: true});
        });
        config.on("change:body", function(){
            router.navigate("#body/" + config.get("body"), {trigger: true});
            config.redraw_features();

        });
        $('.button').click(function(){
            var which_body = $(this).attr('id').split("-")[0];
            config.set({body: which_body});

        });
        $('#zoombox').keyup(function(event){
            if(event.which == 13)
            {
                // Enter pressed
                config.codeAddress();
            }
          });

        if(!Backbone.history.start())
        {
            // By default start with presidential with no specific county
            config.set({body: "us.president"});
        }



    });



});
